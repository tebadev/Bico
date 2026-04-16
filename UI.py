import sys
import os
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox,
    QDialog, QLineEdit, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QTimer

try:
    from modules.recorder import AudioUtilidades, inicializador
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
    from recorder import AudioUtilidades, inicializador

TEMAS = {
    "oscuro": {"bg": "#1e1e1e", "fg": "#ffffff", "btn": "#333333", "brd": "#444444"},
    "claro":  {"bg": "#f0f0f0", "fg": "#222222", "btn": "#ffffff", "brd": "#cccccc"}
}

def obtener_estilo(t):
    return f"""
        QWidget {{ background-color: {t['bg']}; color: {t['fg']}; font-family: sans-serif; }}
        QLabel#reloj {{ font-size: 52px; font-weight: 200; margin: 15px; }}
        QLabel#estado {{ font-size: 11px; font-weight: bold; }}
        QPushButton {{ 
            background-color: {t['btn']}; border: 1px solid {t['brd']}; 
            border-radius: 4px; padding: 8px; color: {t['fg']}; 
        }}
        QPushButton:disabled {{ color: #777777; background-color: {t['bg']}; }}
        QPushButton#btn_tema {{ font-size: 20px; background: transparent; border: none; color: {t['fg']}; }}
        QComboBox, QLineEdit {{ background-color: {t['btn']}; border: 1px solid {t['brd']}; color: {t['fg']}; padding: 4px; }}
    """

class BicoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bivo Recorder")
        self.setFixedSize(320, 430)
        
        self.motor = None
        self.segundos = 0
        self.tema = "oscuro"
        try:
            self.micros = list(AudioUtilidades.detectar_microfonos())
        except:
            self.micros = []

        self._setup_ui()
        self._aplicar_tema()

        self.timer_reloj = QTimer()
        self.timer_reloj.timeout.connect(self._actualizar_reloj)

    def _setup_ui(self):
        root = QVBoxLayout(self)
        
        header = QHBoxLayout()
        header.addStretch()
        self.btn_tema = QPushButton()
        self.btn_tema.setObjectName("btn_tema")
        self.btn_tema.setFixedSize(32, 32)
        self.btn_tema.clicked.connect(self._toggle_tema)
        header.addWidget(self.btn_tema)
        root.addLayout(header)

        self.lbl_t = QLabel("00:00")
        self.lbl_t.setObjectName("reloj")
        self.lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_t)

        self.lbl_e = QLabel("LISTO")
        self.lbl_e.setObjectName("estado")
        self.lbl_e.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.lbl_e)

        root.addSpacing(15)
        root.addWidget(QLabel("Micrófono:"))
        self.cb_mic = QComboBox()
        self.cb_mic.addItem("Por defecto")
        for _, nombre in self.micros: self.cb_mic.addItem(nombre)
        root.addWidget(self.cb_mic)

        root.addWidget(QLabel("Formato:"))
        self.cb_fmt = QComboBox()
        self.cb_fmt.addItems(["WAV", "MP3", "FLAC", "OGG"])
        root.addWidget(self.cb_fmt)

        root.addStretch()

        btns = QHBoxLayout()
        self.b_rec = QPushButton("⏺ Grabar")
        self.b_pau = QPushButton("⏸ Pausar")
        self.b_stp = QPushButton("⏹ Parar")
        
        for b in [self.b_rec, self.b_pau, self.b_stp]:
            btns.addWidget(b)
            
        self.b_rec.clicked.connect(self.on_rec)
        self.b_pau.clicked.connect(self.on_pau)
        self.b_stp.clicked.connect(self.on_stp)
        
        self.b_pau.setEnabled(False)
        self.b_stp.setEnabled(False)
        root.addLayout(btns)

    def _aplicar_tema(self):
        self.setStyleSheet(obtener_estilo(TEMAS[self.tema]))
        self.btn_tema.setText("☼" if self.tema == "oscuro" else "☾")

    def _toggle_tema(self):
        self.tema = "claro" if self.tema == "oscuro" else "oscuro"
        self._aplicar_tema()

    def _actualizar_reloj(self):
        if self.motor and self.motor.estado == "grabando":
            self.segundos += 1
            m, s = divmod(self.segundos, 60)
            self.lbl_t.setText(f"{m:02d}:{s:02d}")

    def on_rec(self):
        idx = self.cb_mic.currentIndex()
        mid = None if idx == 0 else self.micros[idx-1][0]
        
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

    def on_pau(self):
        if not self.motor: return
        if self.motor.estado == "grabando":
            self.motor.pausar()
            self.lbl_e.setText("PAUSADO")
            self.b_pau.setText("▶ Reanudar")
        else:
            self.motor.reanudar()
            self.lbl_e.setText("GRABANDO...")
            self.b_pau.setText("⏸ Pausar")

    def on_stp(self):
        if not self.motor: return
        self.motor.detener()
        self.timer_reloj.stop()
        self.lbl_e.setText("FINALIZANDO...")
        self.lbl_e.setStyleSheet("color: #888888;")
        self.b_pau.setEnabled(False)
        self.b_stp.setEnabled(False)
        QTimer.singleShot(1200, self._finalizar_guardado)

    def _finalizar_guardado(self):
        tmp = self.motor.archivo_temporal
        fmt = self.cb_fmt.currentText().lower()

        if tmp and os.path.exists(tmp):
            self._dialogo_nombre(tmp, fmt)
        
        self.lbl_e.setText("LISTO")
        self.lbl_e.setStyleSheet("")
        self.lbl_t.setText("00:00")
        self.b_rec.setEnabled(True)
        self.b_pau.setText("⏸ Pausar")
        self.cb_mic.setEnabled(True)
        self.cb_fmt.setEnabled(True)
        self.motor = None

    def _dialogo_nombre(self, tmp, fmt):
        dlg = QDialog(self)
        dlg.setWindowTitle("Guardar")
        dlg.setFixedWidth(250)
        l = QVBoxLayout(dlg)
        l.addWidget(QLabel("Nombre del archivo:"))
        edit = QLineEdit("grabacion")
        edit.selectAll()
        l.addWidget(edit)
        
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        bb.accepted.connect(dlg.accept)
        bb.rejected.connect(dlg.reject)
        l.addWidget(bb)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            nombre = edit.text().strip() or "grabacion"
            if not os.path.exists("grabaciones"):
                os.makedirs("grabaciones")
            AudioUtilidades.guardar_archivo(tmp, "grabaciones", nombre, fmt)
        else:
            if os.path.exists(tmp): os.remove(tmp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = BicoApp()
    win.show()
    sys.exit(app.exec())
