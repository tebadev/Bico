import os
from collections import deque

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor

from ui.styles import TEMAS, obtener_estilo
from ui.dialogs import DialogoGuardar
from modules.recorder import AudioUtilidades, inicializador
from modules.history_manager import HistoryManager
from ui.history_dialog import HistoryDialog


# ──────────────────────────────────────────────
# Widget de barras de nivel verticales
# ──────────────────────────────────────────────

class BarrasNivel(QWidget):
    N_BARRAS = 12
    SUAVIZADO = 6

    COLORES_ACTIVOS = [
        "#2ECC8B", "#2ECC8B", "#2ECC8B", "#2ECC8B",
        "#F0C040", "#F0C040", "#F0C040",
        "#FF6B6B", "#FF6B6B", "#FF6B6B", "#FF6B6B", "#FF6B6B",
    ]
    COLOR_INACTIVO = QColor(120, 120, 120, 35)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(56)
        self._nivel = 0.0
        self._historial = deque([0.0] * self.SUAVIZADO, maxlen=self.SUAVIZADO)
        self.setAccessibleName("Nivel de audio del micrófono")

    def set_nivel(self, valor: float):
        self._historial.append(max(0.0, min(1.0, valor)))
        self._nivel = sum(self._historial) / len(self._historial)
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        n = self.N_BARRAS

        gap = 5
        total_gaps = gap * (n + 1)
        barra_w = max(4, (w - total_gaps) // n)
        radio = 3

        for i in range(n):
            umbral = (i + 1) / n
            activa = self._nivel >= umbral

            x = gap + i * (barra_w + gap)
            altura_max = int(h * 0.35 + h * 0.65 * (i / (n - 1)))
            y = h - altura_max

            if activa:
                color = QColor(self.COLORES_ACTIVOS[i])
                color.setAlpha(230)
            else:
                color = self.COLOR_INACTIVO

            p.setBrush(color)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(QRectF(x, y, barra_w, altura_max), radio, radio)

        p.end()


# ──────────────────────────────────────────────
# Ventana principal
# ──────────────────────────────────────────────

class BicoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bico Recorder")
        self.setMinimumSize(320, 460)                    # Ahora se puede redimensionar

        self.motor = None
        self.segundos = 0
        self.tema = "oscuro"
        self._guardando = False
        self._motor_pendiente = None                     # Motor que estamos esperando para guardar

        # Gestor del historial de grabaciones
        self.history_manager = HistoryManager()

        try:
            self.micros = list(AudioUtilidades.detectar_microfonos())
        except Exception as e:
            print(f"Error al detectar micrófonos: {e}")
            self.micros = []

        self._setup_ui()
        self._aplicar_tema()

        # ── Temporizadores ────────────────────────
        self.timer_reloj = QTimer()
        self.timer_reloj.timeout.connect(self._actualizar_reloj)

        self.timer_barras = QTimer()
        self.timer_barras.setInterval(50)              # ← Intervalo que faltaba
        self.timer_barras.timeout.connect(self._actualizar_barras)

        # Temporizador para esperar la finalización real del hilo de grabación
        self._save_watcher = QTimer()
        self._save_watcher.setInterval(100)
        self._save_watcher.timeout.connect(self._check_hilo_terminado)

        # Timeout de seguridad (5 s)
        self._save_timeout = QTimer()
        self._save_timeout.setSingleShot(True)
        self._save_timeout.timeout.connect(self._guardar_por_timeout)

    # ──────────────────────────────────────────────
    # UI setup
    # ──────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)

        # Header con botones de historial y tema
        header = QHBoxLayout()
        # Botón de historial (izquierda)
        self.btn_historial = QPushButton()
        self.btn_historial.setObjectName("btn_historial")
        self.btn_historial.setFixedSize(32, 32)
        self.btn_historial.setText("...")
        self.btn_historial.setAccessibleName("Historial")
        self.btn_historial.clicked.connect(self._mostrar_historial)
        header.addWidget(self.btn_historial)

        header.addStretch()

        # Botón de tema (derecha)
        self.btn_tema = QPushButton()
        self.btn_tema.setObjectName("btn_tema")
        self.btn_tema.setFixedSize(32, 32)
        self.btn_tema.clicked.connect(self._toggle_tema)
        self.btn_tema.setAccessibleName("Cambiar tema")
        header.addWidget(self.btn_tema)
        root.addLayout(header)

        # Reloj
        self.lbl_t = QLabel("00:00")
        self.lbl_t.setObjectName("reloj")
        self.lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_t.setAccessibleName("Temporizador")
        root.addWidget(self.lbl_t)

        # Estado
        self.lbl_e = QLabel("LISTO")
        self.lbl_e.setObjectName("estado")
        self.lbl_e.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_e.setAccessibleName("Estado de la grabadora")
        root.addWidget(self.lbl_e)

        root.addSpacing(12)

        # Barras de nivel
        self.barras_nivel = BarrasNivel()
        root.addWidget(self.barras_nivel)

        root.addSpacing(8)

        # Selector de micrófono
        root.addWidget(QLabel("Micrófono:"))
        self.cb_mic = QComboBox()
        self.cb_mic.setAccessibleName("Micrófono")
        self.cb_mic.addItem("Por defecto")
        for _, nombre in self.micros:
            self.cb_mic.addItem(nombre)
        root.addWidget(self.cb_mic)

        # Selector de formato
        root.addWidget(QLabel("Formato:"))
        self.cb_fmt = QComboBox()
        self.cb_fmt.setAccessibleName("Formato de exportación")
        self.cb_fmt.addItems(["WAV", "MP3", "FLAC", "OGG"])
        root.addWidget(self.cb_fmt)

        root.addStretch()

        root.addWidget(QLabel("Carpeta de destino:"))

        carpeta_layout = QHBoxLayout()
        carpeta_default = os.path.join(os.path.expanduser("~"), "grabaciones")
        self.txt_carpeta = QLineEdit(carpeta_default)
        self.txt_carpeta.setReadOnly(True)
        self.txt_carpeta.setAccessibleName("Carpeta de destino")
        self.btn_carpeta = QPushButton("...")
        self.btn_carpeta.setFixedWidth(32)
        self.btn_carpeta.setAccessibleName("Elegir carpeta")
        self.btn_carpeta.clicked.connect(self._elegir_carpeta)
        carpeta_layout.addWidget(self.txt_carpeta)
        carpeta_layout.addWidget(self.btn_carpeta)
        root.addLayout(carpeta_layout)

        os.makedirs(self.txt_carpeta.text(), exist_ok=True)

        # Botones de control
        btns = QHBoxLayout()
        self.b_rec = QPushButton("⏺ Grabar")
        self.b_pau = QPushButton("⏸ Pausar")
        self.b_stp = QPushButton("⏹ Parar")

        self.b_rec.setAccessibleName("Grabar")
        self.b_pau.setAccessibleName("Pausar")
        self.b_stp.setAccessibleName("Parar")

        for b in [self.b_rec, self.b_pau, self.b_stp]:
            btns.addWidget(b)

        self.b_rec.clicked.connect(self.on_rec)
        self.b_pau.clicked.connect(self.on_pau)
        self.b_stp.clicked.connect(self.on_stp)

        self.b_pau.setEnabled(False)
        self.b_stp.setEnabled(False)
        root.addLayout(btns)

    # ──────────────────────────────────────────────
    # Tema
    # ──────────────────────────────────────────────

    def _aplicar_tema(self):
        self.setStyleSheet(obtener_estilo(TEMAS[self.tema]))
        self.btn_tema.setText("☼" if self.tema == "oscuro" else "☾")

    def _toggle_tema(self):
        self.tema = "claro" if self.tema == "oscuro" else "oscuro"
        self._aplicar_tema()

    # ──────────────────────────────────────────────
    # Reloj
    # ──────────────────────────────────────────────

    def _actualizar_reloj(self):
        if self.motor and self.motor.estado == "grabando":
            self.segundos += 1
            m, s = divmod(self.segundos, 60)
            self.lbl_t.setText(f"{m:02d}:{s:02d}")

    # ──────────────────────────────────────────────
    # Historial
    # ──────────────────────────────────────────────

    def _mostrar_historial(self):
        dlg = HistoryDialog(self, self.history_manager)
        dlg.exec()

    # ──────────────────────────────────────────────
    # Acciones de grabación
    # ──────────────────────────────────────────────

    def on_rec(self):
        if self._guardando:
            return

        # Cancelar cualquier espera de guardado pendiente (motor ya detenido)
        self._save_watcher.stop()
        self._save_timeout.stop()
        self._motor_pendiente = None

        idx = self.cb_mic.currentIndex()
        mid = None if idx == 0 else self.micros[idx - 1][0]

        self.motor = inicializador(44100, 1, mid)
        self.segundos = 0
        self.lbl_t.setText("00:00")
        self.lbl_e.setText("GRABANDO...")
        self.lbl_e.setStyleSheet("color: #ff5555;")

        self.b_rec.setEnabled(False)
        self.b_pau.setEnabled(True)
        self.b_stp.setEnabled(True)
        self.cb_mic.setEnabled(False)
        self.cb_fmt.setEnabled(False)
        self.timer_reloj.start(1000)
        self.timer_barras.start()

    def on_pau(self):
        if not self.motor or self._guardando:
            return
        if self.motor.estado == "grabando":
            self.motor.pausar()
            self.lbl_e.setText("PAUSADO")
            self.b_pau.setText("▶ Reanudar")
            self.b_pau.setAccessibleName("Reanudar")
        else:
            self.motor.reanudar()
            self.lbl_e.setText("GRABANDO...")
            self.b_pau.setText("⏸ Pausar")
            self.b_pau.setAccessibleName("Pausar")

    def on_stp(self):
        if not self.motor or self._guardando:
            return

        self._guardando = True
        self.motor.detener()
        self.timer_reloj.stop()
        self.timer_barras.stop()
        self.barras_nivel.set_nivel(0.0)

        self.lbl_e.setText("FINALIZANDO...")
        self.lbl_e.setStyleSheet("color: #888888;")
        self.b_pau.setEnabled(False)
        self.b_stp.setEnabled(False)

        # Guardamos la referencia del motor que estamos esperando
        self._motor_pendiente = self.motor
        self.motor = None   # Liberamos la referencia principal

        # Iniciamos el watcher que verificará cuándo terminó realmente el hilo
        self._save_watcher.start()
        self._save_timeout.start(5000)   # 5 segundos máximo de espera

    # ── Métodos de espera activa para el hilo ──

    def _check_hilo_terminado(self):
        """Verifica si el hilo de grabación ya terminó (mirando el evento interno)."""
        motor = self._motor_pendiente
        if motor is None:
            self._save_watcher.stop()
            return

        # El evento _stop_event se activa justo al salir del bucle de grabación.
        # En ese momento el archivo ya está completamente escrito y cerrado.
        if motor._stop_event.is_set():
            self._save_watcher.stop()
            self._save_timeout.stop()
            self._finalizar_guardado(motor)

    def _guardar_por_timeout(self):
        """Se ejecuta si pasó el tiempo máximo de espera."""
        self._save_watcher.stop()
        if self._motor_pendiente:
            self._finalizar_guardado(self._motor_pendiente)

    def _finalizar_guardado(self, motor_ref):
        if not motor_ref:
            return

        tmp = motor_ref.archivo_temporal
        fmt = self.cb_fmt.currentText().lower()
        carpeta = self.txt_carpeta.text()

        if tmp and os.path.exists(tmp):
            self._dialogo_nombre(tmp, fmt, carpeta)
        else:
            self._reset_ui()

    def _dialogo_nombre(self, tmp: str, fmt: str, carpeta: str):
        dlg = DialogoGuardar(self)
        if dlg.exec() == DialogoGuardar.DialogCode.Accepted:
            # Construimos la ruta final exactamente igual que en AudioUtilidades
            nombre_final = dlg.nombre if dlg.nombre.endswith(f".{fmt}") else dlg.nombre + f".{fmt}"
            ruta_final = os.path.join(carpeta, nombre_final)

            AudioUtilidades.guardar_archivo(tmp, carpeta, dlg.nombre, fmt)

            # Si el archivo se guardó correctamente, lo añadimos al historial
            if os.path.exists(ruta_final):
                self.history_manager.add(ruta_final, fmt)
        else:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception as e:
                    print(f"Error al eliminar archivo temporal: {e}")

        self._reset_ui()

    def _reset_ui(self):
        """Restaura la interfaz al estado inicial."""
        self.lbl_e.setText("LISTO")
        self.lbl_e.setStyleSheet("")
        self.lbl_t.setText("00:00")
        self.b_rec.setEnabled(True)
        self.b_pau.setText("⏸ Pausar")
        self.b_pau.setAccessibleName("Pausar")
        self.cb_mic.setEnabled(True)
        self.cb_fmt.setEnabled(True)
        self._motor_pendiente = None
        self._guardando = False

    def _elegir_carpeta(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta", self.txt_carpeta.text())
        if carpeta:
            self.txt_carpeta.setText(carpeta)

    # ──────────────────────────────────────────────
    # Barras de nivel (ahora también en pausa)
    # ──────────────────────────────────────────────

    def _actualizar_barras(self):
        if not self.motor or self._guardando:
            return
        # El motor ya pone nivel_actual = 0.0 en pausa, así que las barras se apagan solas
        self.barras_nivel.set_nivel(self.motor.nivel_actual)

    # ──────────────────────────────────────────────
    # Limpieza al cerrar
    # ──────────────────────────────────────────────

    def closeEvent(self, event):
        if self.motor:
            self.motor.detener()
        self._save_watcher.stop()
        self._save_timeout.stop()
        self.timer_reloj.stop()
        self.timer_barras.stop()
        event.accept()