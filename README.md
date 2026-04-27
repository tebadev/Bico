***

# Bico

> 🇦🇷 Español | [🇬🇧 English](README-EN.md)

Bico es una potente grabadora de audio diseñada para ofrecer máxima estabilidad y fidelidad. Utiliza una arquitectura **Productor-Consumidor** mediante hilos independientes, garantizando una captura de datos fluida sin riesgo de pérdida de paquetes o saltos en el audio, incluso bajo carga del sistema.

## Características Principales

- **Motor Asíncrono de Alto Rendimiento**: Procesamiento de audio en hilos dedicados para evitar bloqueos.
- **Normalización Dinámica de Nivel**: Cálculo de nivel por RMS con pico decayente, funciona correctamente con el micrófono a cualquier volumen del sistema.
- **Visualizador de Nivel de Audio**: Barras verticales escalonadas con colores verde → amarillo → rojo y suavizado por promedio móvil.
- **Sistema de Temas**: Interfaz gráfica con modo Oscuro y Claro dinámico.
- **Gestión de Hardware**: Escaneo dinámico y selección de dispositivos de entrada de audio (micrófonos).
- **Selector de Carpeta de Destino**: Elección del directorio de guardado desde la interfaz antes de grabar.
- **Soporte Multiformato**: Exportación versátil a `.wav`, `.flac`, `.ogg` y `.mp3` (vía FFmpeg).
- **Seguridad de Datos**: Generación de archivos temporales únicos para prevenir la sobrescritura.

## Arquitectura del Proyecto

El proyecto separa la lógica de negocio de la interfaz de usuario:

```
Bico/
├── main.py           → Punto de entrada de la aplicación.
├── modules/
│   ├── recorder.py   → Motor de audio, normalización de nivel y utilidades de hardware.
│   └── __init__.py
└── ui/
    ├── app_window.py → Ventana principal y visualizador de barras de nivel.
    ├── dialogs.py    → Diálogos auxiliares (nombre de archivo, etc.).
    ├── styles.py     → Sistema de temas oscuro/claro.
    └── __init__.py
```

## Instalación

### Requisitos del Sistema
- **Python 3.8+**
- **PortAudio**: Necesario para la biblioteca `sounddevice`.
- **FFmpeg**: Opcional (requerido para exportación a `.mp3`).

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

## Guía de Uso

### Interfaz Gráfica
```bash
python main.py
```

## Preview UI:

<img width="334" height="498" alt="imagen" src="https://github.com/user-attachments/assets/76683b54-799e-4b54-a764-666e38186644" />

## Contribuidores

Bico es el resultado del desarrollo conjunto enfocado en la eficiencia y la experiencia de usuario:

- **[Igoru1](https://github.com/Igoru1)** - *Backend Architect*: Desarrollo del motor de audio asíncrono, gestión de buffers y lógica central de grabación.
- **[Ars-byte](https://github.com/Ars-byte)** - *UI Lead (PyQt6) & Integration*: Desarrollo completo de la interfaz gráfica en PySide6, diseño del sistema de temas, resolución de bugs de concurrencia y optimización del flujo de guardado.
- **[tebadev](https://github.com/tebadev)** - *Original Lead*: Diseño y lógica inicial del proyecto.

## Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

***