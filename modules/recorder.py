import sounddevice as sd
import soundfile as sf
import shutil
import subprocess
import os
import threading
import tempfile
import queue
import numpy as np


class AudioUtilidades:
    @staticmethod
    def guardar_archivo(ruta_origen, directorio_destino, nombre_final, formato="wav"):
        """
        Mueve el archivo temporal a su destino final, convirtiéndolo si es necesario.
        """
        if not nombre_final.endswith(f".{formato}"):
            nombre_final += f".{formato}"

        ruta_completa = os.path.join(directorio_destino, nombre_final)
        os.makedirs(directorio_destino, exist_ok=True)

        try:
            if formato.lower() == "wav":
                shutil.move(ruta_origen, ruta_completa)
            else:
                try:
                    data, samplerate = sf.read(ruta_origen)
                    sf.write(ruta_completa, data, samplerate)
                    os.remove(ruta_origen)
                except Exception as e:
                    print(f"soundfile no pudo convertir a {formato}, intentando con ffmpeg: {e}")
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", ruta_origen, ruta_completa],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    os.remove(ruta_origen)
        except Exception as e:
            print(f"ha ocurrido un error al guardar el archivo: {e}")

    @staticmethod
    def detectar_microfonos():
        """Retorna una lista de tuplas con los micrófonos disponibles."""
        dispositivos = sd.query_devices()
        micros = tuple(
            (i, d['name'])
            for i, d in enumerate(dispositivos)
            if d['max_input_channels'] > 0
        )
        return micros


class Grabadora:
    """
    Motor de grabación asíncrono.
    Usa un sistema de Productor (Callback) y Consumidor (Bucle de guardado)
    para evitar cortes de audio cuando la PC está lenta.
    """

    _PICO_MINIMO = 0.01
    _DECAIMIENTO = 0.10

    def __init__(self, frecuencia, canales, dispositivo_id=None):
        self.frecuencia = frecuencia
        self.canales = canales
        self.estado = "detenido"
        self.dispositivo_id = dispositivo_id
        self.archivo_temporal = None
        self.cola_datos = queue.Queue()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()  # protege nivel_actual

        self.nivel_actual = 0.0
        self._pico = self._PICO_MINIMO

    def callback(self, indata, frames, _time, status):
        if self.estado != "grabando":
            return

        try:
            self.cola_datos.put(indata.copy(), timeout=0.1)
        except queue.Full:
            pass

        rms = float(np.sqrt(np.mean(indata ** 2)))

        if rms > self._pico:
            self._pico = rms
        else:
            bloque_seg = frames / self.frecuencia
            self._pico = max(
                self._pico * (1.0 - self._DECAIMIENTO * bloque_seg),
                self._PICO_MINIMO
            )

        with self._lock:
            self.nivel_actual = min(rms / self._pico, 1.0)

    def grabar(self):
        self.estado = "grabando"
        self._stop_event.clear()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            self.archivo_temporal = tf.name

        try:
            with sf.SoundFile(self.archivo_temporal, mode="w",
                              samplerate=self.frecuencia, channels=self.canales) as archivo:
                with sd.InputStream(samplerate=self.frecuencia, channels=self.canales,
                                    device=self.dispositivo_id, callback=self.callback) as micro:
                    # Bucle principal: sale cuando se detiene la grabación y la cola está vacía
                    while not self._stop_event.is_set() or not self.cola_datos.empty():
                        try:
                            audio_listo = self.cola_datos.get(timeout=0.1)
                            archivo.write(audio_listo)
                        except queue.Empty:
                            continue
        except Exception as e:
            print(f"Ha ocurrido un error con la grabación: {e}")
            # Limpiar archivo temporal si ocurre un error
            if self.archivo_temporal and os.path.exists(self.archivo_temporal):
                try:
                    os.remove(self.archivo_temporal)
                except OSError:
                    pass
                self._stop_event.set()

    def pausar(self):
        if self.estado == "grabando":
            self.estado = "pausado"
            with self._lock:
                self.nivel_actual = 0.0

    def reanudar(self):
        if self.estado == "pausado":
            self.estado = "grabando"

    def detener(self):
        self.estado = "detenido"
        self._stop_event.set()


def inicializador(frecuencia, canales, dispositivo_id):
    grabadora = Grabadora(frecuencia=frecuencia, canales=canales, dispositivo_id=dispositivo_id)
    hilo = threading.Thread(target=grabadora.grabar, daemon=True)
    hilo.start()
    return grabadora