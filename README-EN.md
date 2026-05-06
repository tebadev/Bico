# Bico

> [Español](README.md) | English

Bico is a powerful audio recorder designed for maximum stability and fidelity. It utilizes a **Producer-Consumer** architecture with independent threads, ensuring smooth data capture without the risk of packet loss or audio dropouts, even under system load.

## Main Features

- **High-Performance Asynchronous Engine:** Audio processing on dedicated threads to prevent crashes.
- **Dynamic Level Normalization:** RMS-based level calculation with decay peak, works correctly at any system volume.
- **Audio Level Visualizer:** Stepped vertical bars with green → yellow → red colors and moving average smoothing.
- **Theme System:** Graphical interface with dynamic Dark and Light modes.
- **Hardware Management:** Dynamic scanning and selection of audio input devices (microphones).
- **Destination Folder Selector:** Choose the save directory from the interface before recording.
- **Multi-Format Support:** Versatile export to `.wav`, `.flac`, `.ogg`, and `.mp3` (via FFmpeg).
- **Data Security:** Generation of unique temporary files to prevent overwriting.
- **Recording History:** Persistent JSON log with file existence verification; manually deleted recordings are shown as strikethrough.

## Project Architecture

The project separates business logic from the user interface:

```
Bico/
├── main.py                  → Application entry point.
├── modules/
│   ├── recorder.py          → Audio engine, level normalization, and hardware utilities.
│   ├── history_manager.py   → Recording history management (JSON).
│   └── __init__.py
└── ui/
    ├── app_window.py        → Main window and level bar visualizer.
    ├── dialogs.py           → Auxiliary dialogs (file name, etc.).
    ├── history_dialog.py    → History viewing dialog.
    ├── styles.py            → Dark/Light theme system.
    └── __init__.py
```

## Installation

### System Requirements

- **Python 3.8+**
- **PortAudio**: Required for the `sounddevice` library.
- **FFmpeg**: Optional (required for exporting to `.mp3`).
- **Ubuntu/Debian:** `sudo apt install portaudio19-dev ffmpeg`

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## User Guide

### Graphical Interface

Designed for an intuitive and modern desktop experience.

```bash
python main.py
```

## UI Preview

<img width="336" height="499" alt="imagen" src="https://github.com/user-attachments/assets/b7dccb5e-2a95-43c6-a931-b023cceca492" />


## Contributors

Bico is the result of collaborative development focused on efficiency and user experience:

- **[Igor](https://github.com/albeiroigor)** - *Frontend Architect*: Complete development of the graphical interface in PySide6, theme system design, concurrency bug fixes, save flow optimization, and implementation of the recording history feature.
- **[tebadev](https://github.com/tebadev)** - *Backend Architect and Original Lead*: Initial project design and logic.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

***