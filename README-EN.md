# Bico

Bico is a powerful audio recorder designed for maximum stability and fidelity. It utilizes a Producer-Consumer architecture with independent threads, ensuring smooth data capture without the risk of packet loss or audio dropouts, even under system load.

## Main Features
- **High-Performance Asynchronous Engine:** Audio processing on dedicated threads to prevent crashes.
- **Dual Interface:** Support for modern graphical environments (PyQt6) and terminals (TTY/CLI).
- **Theme System:** Graphical interface with dynamic Dark and Light modes.
- **Hardware Management:** Dynamic scanning and selection of audio input devices.
- **Multi-Format Support:** Versatile export to `.wav`, `.flac`, `.ogg`, and `.mp3` (via FFmpeg).
- **Data Security:** Generation of unique temporary files to prevent overwriting.

## Project Architecture
The project separates business logic from user interfaces to allow for multiple frontends:
```text
Bico/
├── UI.py             # Main graphical interface (PyQt6)
├── main.py           # Command-line interface (TTY)
├── modules/          
│   ├── recorder.py   # Audio engine and hardware utilities
│   └── __init__.py
└── recordings/       # Destination folder for final files
```

## Installation

### System Requirements
* **Python 3.8+**
* **PortAudio**: Required for the `sounddevice` library.
* **FFmpeg**: Optional (required for exporting to `.mp3`).
- **Ubuntu/Debian:** `sudo apt install portaudio19-dev ffmpeg`


### Installing Dependencies
```bash
pip install -r requirements.txt
```

## User Guide

### Graphical Interface (PyQt6)
Designed for an intuitive and modern desktop experience.
```bash
python UI.py
```
*Preview:*
<br>
<img width="963" height="973" alt="image" src="https://github.com/user-attachments/assets/3165beb4-b37c-4cea-ab74-b595321d0e0f" />

### Terminal Interface (TTY)
Ideal for remote environments or users who prefer the console.
```bash
python main.py
```

| Command | Action |
| :--- | :--- |
| `p` | Pause current recording |
| `r` | Resume recording |
| `s` | Stop and save the file |

*Preview:*
<br>
<img width="328" height="444" alt="image" src="https://github.com/user-attachments/assets/419e9170-3568-4688-91e5-82a9cd0db6b7" />

## Contributors

Bico is the result of collaborative development focused on efficiency and user experience:

- **[Igoru1](https://github.com/Igoru1)** - *Backend Architect*: Development of the asynchronous audio engine, buffer management, and core recording logic.
- **[Ars-byte](https://github.com/Ars-byte)** - *UI Lead (PyQt6) & Integration*: Complete development of the graphical interface in PyQt6, theme system design, resolution of clicks/concurrency bugs, and optimization of the save flow.
- **[tebadev](https://github.com/tebadev)** - *Original Lead*: Initial project design and logic.

## 📄 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

***
