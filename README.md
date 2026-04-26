***

# Bico

> 🇦🇷 Español | [🇬🇧 English](README-EN.md)

Bico es una potente grabadora de audio diseñada para ofrecer máxima estabilidad y fidelidad. Utiliza una arquitectura **Productor-Consumidor** mediante hilos independientes, garantizando una captura de datos fluida sin riesgo de pérdida de paquetes o saltos en el audio, incluso bajo carga del sistema.

## Características Principales

- **Motor Asíncrono de Alto Rendimiento**: Procesamiento de audio en hilos dedicados para evitar bloqueos.
- **Dual Interface**: Soporte para entorno gráfico moderno (**PyQt6**) y terminales (**TTY/CLI**).
- **Sistema de Temas**: Interfaz gráfica con modo Oscuro y Claro dinámico.
- **Gestión de Hardware**: Escaneo dinámico y selección de dispositivos de entrada de audio (micrófonos).
- **Soporte Multiformato**: Exportación versátil a `.wav`, `.flac`, `.ogg` y `.mp3` (vía FFmpeg).
- **Seguridad de Datos**: Generación de archivos temporales únicos para prevenir la sobrescritura.

## Arquitectura del Proyecto

El proyecto separa la lógica de negocio de las interfaces de usuario para permitir múltiples frontends:

```
Bico/
├── UI.py             → Interfaz gráfica principal (PyQt6).
├── main.py           → Interfaz de línea de comandos (TTY).
├── modules/
│   ├── recorder.py   → Motor de audio y utilidades de hardware.
│   └── __init__.py
└── grabaciones/      → Carpeta de destino de los archivos finales.
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

### Interfaz Gráfica (PyQt6)
Diseñada para una experiencia de escritorio intuitiva y moderna.
```bash
python UI.py
```
## Preview UI:

<img width="334" height="498" alt="imagen" src="https://github.com/user-attachments/assets/76683b54-799e-4b54-a764-666e38186644" />


### Interfaz de Terminal (TTY)
Ideal para entornos remotos o usuarios que prefieren la consola.
```bash
python main.py
```
| Comando | Acción |
|---------|--------|
| `p`     | Pausar la grabación actual |
| `r`     | Reanudar la grabación |
| `s`     | Detener y proceder a guardar el archivo |

## Preview tty:

<img width="328" height="444" alt="image" src="https://github.com/user-attachments/assets/419e9170-3568-4688-91e5-82a9cd0db6b7" />


## Contribuidores

Bico es el resultado del desarrollo conjunto enfocado en la eficiencia y la experiencia de usuario:

- **[Igoru1](https://github.com/Igoru1)** - *Backend Architect*: Desarrollo del motor de audio asíncrono, gestión de buffers y lógica central de grabación.
- **[Ars-byte](https://github.com/Ars-byte)** - *UI Lead (PyQt6) & Integration*: Desarrollo completo de la interfaz gráfica en PyQt6, diseño del sistema de temas, resolución de clics/bugs de concurrencia y optimización del flujo de guardado.
- **[tebadev](https://github.com/tebadev)** - *Original Lead*: Diseño y lógica inicial del proyecto.

## Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

***
