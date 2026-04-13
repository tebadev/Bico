import sounddevice as sd
import soundfile as sf
import shutil
import subprocess
import os
import threading
import tempfile
import queue

# Varias utilidades para la grabadora
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
                # Si es wav, solo movemos el archivo
                shutil.move(ruta_origen, ruta_completa)
            else: 
                # Intentamos con soundfile (WAV, FLAC, OGG sin dependencias extra)
                try:
                    data, samplerate = sf.read(ruta_origen)
                    sf.write(ruta_completa, data, samplerate)
                    os.remove(ruta_origen)
                except Exception:
                    # Si soundfile no soporta el formato (ej. MP3), usamos ffmpeg
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", ruta_origen, ruta_completa],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    os.remove(ruta_origen)
        except Exception:
            print ("ha ocurrido un error cuando se intento guardar el archivo.")

    @staticmethod
    def detectar_microfonos():
        """ Retorna una lista de tuplas con los micrófonos disponibles. """

        dispositivos = sd.query_devices()

        micros = tuple(
            (i, d['name']) 
            for i, d in enumerate(dispositivos) 
            if d['max_input_channels'] > 0
        )
        return micros


# Motor de la grabadora 
class Grabadora:
    """
    Motor de grabación asíncrono. 
    Usa un sistema de Productor (Callback) y Consumidor (Bucle de guardado)
    para evitar cortes de audio cuando la PC está lenta.
    """

    def __init__(self, frecuencia, canales, dispositivo_id=None):
        """
        Configura los parámetros de audio.
        frecuencia: Sample rate (ej. 44100).
        canales: 1 para mono, 2 para estéreo.
        dispositivo_id: Índice del micrófono según sd.query_devices().
        """
        self.frecuencia = frecuencia
        self.canales = canales
        self.estado = "detenido"
        self.dispositivo_id = dispositivo_id
        self.archivo_temporal = None
        # La cola sirve de buffer para que la escritura en disco no bloquee la captura de audio
        self.cola_datos = queue.Queue()

    def callback(self, indata, _frames, _time, status):
        """
        Esta función la llama el sistema operativo cada vez que el micro tiene audio.
        Debe ser lo más rápida posible para no causar clics.
        """

        if self.estado == "grabando":
            self.cola_datos.put(indata.copy())

    # Método que inicializa la gravación.
    def grabar(self):
        self.estado = "grabando"

        # Crear un archivo temporal único para evitar colisiones de nombres
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            self.archivo_temporal = tf.name

        try:
            with sf.SoundFile(self.archivo_temporal, mode="w", samplerate=self.frecuencia, channels=self.canales) as archivo:
                with sd.InputStream(samplerate=self.frecuencia, channels=self.canales, device=self.dispositivo_id, callback=self.callback) as micro:
                    # El bucle continúa si no se ha detenido O si aún quedan datos en la cola por escribir
                    while self.estado != "detenido" or not self.cola_datos.empty():
                        try: 
                            # Extrae el bloque de audio de la cola (espera max 0.1s)
                            audio_listo = self.cola_datos.get(timeout=0.1)
                            archivo.write(audio_listo)
                        except queue.Empty:
                            # Si la cola está vacía temporalmente, sigue esperando hasta que el estado cambie
                            continue
          
        except Exception as e:
            print(f"Ha ocurrido un error con la grabación: {e}")

    # Métodos que controlan la grabación.
    def pausar(self):
        if self.estado == "grabando":
            self.estado = "pausado"

    def reanudar(self):
        if self.estado == "pausado":
            self.estado = "grabando"
 
    def detener(self):
        self.estado = "detenido"

# Función que inicializa una instancia de grabación en un hilo independiente.
def inicializador(frecuencia, canales, dispositivo_id):
    bico = Grabadora(frecuencia=frecuencia, canales=canales, dispositivo_id=dispositivo_id)
    hilo = threading.Thread(target=bico.grabar)
    hilo.start()
    return bico

if __name__ == "__main__":
    pass
