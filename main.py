import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np 
from pynput import keyboard

# Configuración
frecuencia = 44100
canales = 2
nombre_prueba = "pureba.wav"
datos_audio = []
grabando = True 

def al_presionar(tecla):
    global grabando
    try:
        if tecla.char == "s":
            grabando = False
            return False
    except AttributeError:
        pass

escuchador = keyboard.Listener(on_press=al_presionar)
escuchador.start()

# Grabación 

with sd.InputStream(samplerate=frecuencia, channels=canales) as micro:
    while grabando:
        trozo, desborde = micro.read(512)
        datos_audio.append(trozo.copy())

# Guardado
if datos_audio:
    audio_final = np.concatenate(datos_audio, axis=0)
    write(nombre_prueba, frecuencia, audio_final)
    print ("todo listo")
