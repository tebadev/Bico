# 🎙️ Bico: Simple Python Audio Recorder

Bico es una herramienta ligera y eficiente escrita en Python para grabar audio en tiempo real. Utiliza la entrada de sonido del sistema y permite detener la grabación de forma interactiva mediante el teclado, guardando el resultado en un archivo de alta fidelidad `.wav`.

## ✨ Características

* **Grabación en tiempo real:** Captura audio directamente desde el micrófono predeterminado.
* **Control por teclado:** Finaliza la grabación de forma segura presionando la tecla `s`.
* **Salida de alta calidad:** Utiliza una frecuencia de muestreo de 44.1 kHz en estéreo por defecto.
* **Manejo eficiente de datos:** Utiliza `numpy` para procesar y concatenar los fragmentos de audio grabados.

## 🚀 Requisitos previos

Antes de ejecutar el programa, asegúrate de tener instaladas las dependencias necesarias:

pip install sounddevice scipy numpy pynput

Nota: En sistemas Linux, es posible que necesites instalar las cabeceras de portaudio:

sudo apt-get install libportaudio2

## 🛠️ Cómo usarlo

1. Ejecuta el script:
   python bico.py

2. **Grabando:** El programa comenzará a capturar audio inmediatamente.

3. **Detener:** Cuando desees finalizar, presiona la tecla `s` en tu teclado.

4. **Resultado:** El archivo se guardará automáticamente con el nombre `pureba.wav` en el mismo directorio.

## ⚙️ Configuración

Puedes personalizar los parámetros de grabación directamente en el código.

## 📦 Tecnologías utilizadas

* `pynput`: Para escuchar eventos del teclado en segundo plano.
* `sounddevice`: Para gestionar el flujo de entrada del micrófono.
* `numpy`: Para el manejo y concatenación de arreglos de datos.
* `scipy`: Para la exportación y guardado del archivo final.

## 📝 Próximas mejoras

* [ ] Permitir nombres de archivo personalizados mediante argumentos
* [ ] Agregar una interfaz gráfica sencilla
* [ ] Soporte para diferentes formatos de audio (MP3, FLAC)

