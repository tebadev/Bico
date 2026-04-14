# Bico

Grabadora de audio asíncrona por línea de comandos, construida en Python.

Utiliza un modelo productor-consumidor con hilos independientes para garantizar capturas estables, sin saltos ni pérdida de datos, incluso bajo carga de procesamiento elevada.

---

## Características

- **Motor asíncrono** — captura en un hilo separado para no bloquear la interfaz
- **Control en tiempo real** — pausar, reanudar y detener durante la grabación
- **Detección de hardware** — escaneo dinámico de micrófonos disponibles
- **Multiformato** — exportación a `.wav`, `.flac`, `.ogg` y `.mp3` (requiere FFmpeg)
- **Archivos temporales únicos** — evita sobrescritura accidental entre sesiones

---

---
## Preview

<img width="452" height="398" alt="image" src="https://github.com/user-attachments/assets/0ae7d069-2ac2-4df8-85c6-cd5dff86d4a7" />


---

## Requisitos

**Sistema**
- Python 3.8+
- PortAudio (requerido por `sounddevice`)
- FFmpeg *(opcional, solo para exportar a `.mp3`)*

**Python**
```
pip install sounddevice soundfile
```

---

## Uso

```bash
git clone https://github.com/tebadev/Bico.git
cd bico
python main.py
```

Al iniciar, el menú principal permite seleccionar el micrófono de entrada. Durante la grabación:

| Comando | Acción |
|---------|--------|
| `p` | Pausar |
| `r` | Reanudar |
| `s` | Detener y guardar |

Al detener, se solicitará el nombre del archivo y el formato de salida.

---

## Arquitectura

```
main.py          →  Interfaz CLI y flujo de usuario
recorder.py
  ├── Grabadora        →  Motor: captura, cola y escritura en disco
  └── AudioUtilidades  →  Detección de hardware y conversión de formatos
```

---

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/mi-mejora`
3. Envía un pull request

---

## Licencia

MIT — consulta el archivo `LICENSE` para más detalles.

---

## Contribuidores
- [Ars-byte](https://github.com/Ars-byte) - Mejora de documentación y solucionador de bugs.

- [Igoru1](https://github.com/Igoru1) - Desarrollador de backend.

- [Tebadev](https://github.com/tebadev) - Desarrollador de frontend.
