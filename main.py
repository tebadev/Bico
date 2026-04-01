import sys
import threading
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine



class Grabadora(QObject):
    mensajeCambiado = Signal(str)
    nivelAudioCambiado = Signal(float)
    grabandoCambiado = Signal(bool)

    def __init__(self):
        super().__init__()
        self._grabando = False

    @Property(bool, notify=grabandoCambiado)
    def grabando(self):
        return self._grabando

    @Slot(str)
    def iniciarGrabacion(self, nombre_archivo):
        self._grabando = True
        self.grabandoCambiado.emit(True)
        self.mensajeCambiado.emit("Grabando...")
        threading.Thread(target=self._grabar, args=(nombre_archivo,), daemon=True).start()

    @Slot()
    def detenerGrabacion(self):
        self._grabando = False

    def _grabar(self, nombre_prueba):
        frecuencia = 44100
        canales = 2
        datos_audio = []

        with sd.InputStream(samplerate=frecuencia, channels=canales) as micro:
            while self._grabando:
                trozo, desborde = micro.read(512)
                datos_audio.append(trozo.copy())

        if datos_audio:
            audio_final = np.concatenate(datos_audio, axis=0)
            write(nombre_prueba, frecuencia, audio_final)
            self.mensajeCambiado.emit("todo listo")

        self.grabandoCambiado.emit(False)


app = QGuiApplication(sys.argv)
grabadora = Grabadora()
engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("grabadora", grabadora)
engine.load("src/ui/main.qml")
sys.exit(app.exec())