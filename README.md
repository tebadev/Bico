***

# Bico - Grabadora de Audio Asíncrona para Linux

Bico es una potente grabadora de audio asíncrona para entornos Linux, diseñada bajo un modelo de arquitectura **productor-consumidor**. Utiliza hilos independientes para garantizar una captura de datos estable y de alta fidelidad, eliminando el riesgo de pérdida de paquetes o saltos en el audio, incluso en situaciones de alta carga del sistema.

## Características Principales

- **Motor Asíncrono de Alto Rendimiento**: Procesamiento de audio en hilos dedicados para evitar bloqueos en la interfaz de usuario.
- **Dual Interface**: Soporte nativo para terminales (TTY/CLI) y entorno gráfico moderno basado en GTK.
- **Control de Flujo en Tiempo Real**: Interacción dinámica para pausar, reanudar y detener grabaciones sin procesamientos posteriores lentos.
- **Gestión Inteligente de Hardware**: Escaneo dinámico y selección de dispositivos de entrada de audio (micrófonos).
- **Soporte Multiformato**: Exportación versátil a `.wav`, `.flac`, `.ogg` y `.mp3` (vía FFmpeg).
- **Seguridad de Datos**: Generación de archivos temporales únicos para prevenir la sobrescritura de sesiones anteriores.


## Previews

GTK VERSION:

<img width="523" height="536" alt="image" src="https://github.com/user-attachments/assets/769b0aea-3a72-497b-a474-c01161662539" />

TTY/CLI VERSION:


<img width="420" height="495" alt="image" src="https://github.com/user-attachments/assets/76e67de9-773e-4af7-90bb-5498d5984475" />


## Arquitectura del Sistema

El proyecto está organizado de forma modular para separar la lógica de negocio de la presentación:

```
Bico/
├── main.py           → Interfaz CLI (TTY) y flujo de usuario.
├── gui.py            → Interfaz gráfica (GTK).
└── core/
    ├── recorder.py   → Motor de audio: gestión de colas y escritura asíncrona.
    └── utils.py      → Detección de hardware y manejo de formatos.
```

- `recorder.py`: El núcleo del sistema. Contiene el motor de captura y las utilidades de conversión de audio.
- `main.py`: Punto de entrada para la interfaz de línea de comandos (TTY).
- `gui.py` (o `main_gtk.py`): Interfaz gráfica desarrollada en GTK para una experiencia de escritorio integrada.

## Instalación

### Requisitos del Sistema
- Python 3.8+
- PortAudio: Necesario para la biblioteca `sounddevice`.
- FFmpeg: Opcional (requerido para exportación a `.mp3`).
- GTK 3/4: Requerido para ejecutar la versión gráfica.

### Instalación de Dependencias
```bash
pip install sounddevice soundfile
```

## Guía de Uso

### Interfaz de Terminal (TTY)
```bash
python main.py
```

| Comando | Acción |
|---------|--------|
| `p`     | Pausar la grabación actual |
| `r`     | Reanudar la grabación |
| `s`     | Detener y proceder a guardar el archivo |

### Interfaz Gráfica (GTK)
```bash
python gui.py
```

Ofrece controles visuales intuitivos para la selección de dispositivos y gestión de archivos.

## Contribuidores

Bico es el resultado del esfuerzo conjunto de desarrolladores enfocados en la eficiencia y la experiencia de usuario:

- **Igoru1** - Backend Architect: Desarrollo del motor de audio asíncrono y la lógica de integración con la UI.
- **Ars-byte** - UI/UX & Core Support: Desarrollo de la interfaz gráfica en GTK, optimización de documentación técnica y resolución de bugs críticos.
- **Tebadev** - Frontend Lead: Diseño y lógica de la interfaz de usuario original.

## Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

***
