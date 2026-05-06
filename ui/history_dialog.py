from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HistoryDialog(QDialog):
    """Muestra el historial de grabaciones."""

    def __init__(self, parent=None, history_manager=None):
        super().__init__(parent)
        self.history_manager = history_manager
        self.setWindowTitle("Historial de grabaciones")
        self.setMinimumSize(600, 350)

        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Grabaciones anteriores")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Formato", "Fecha", "Duración"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 60)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 80)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Botones inferiores
        btn_layout = QHBoxLayout()
        self.btn_limpiar = QPushButton("Quitar inexistentes")
        self.btn_limpiar.clicked.connect(self._limpiar_inexistentes)
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_limpiar)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cerrar)
        layout.addLayout(btn_layout)

        self._cargar_datos()

    def _cargar_datos(self):
        """Carga los datos del historial en la tabla."""
        if self.history_manager is None:
            return

        entradas = self.history_manager.listar()
        self.table.setRowCount(len(entradas))

        fuente_tachada = QFont()
        fuente_tachada.setStrikeOut(True)

        for i, entrada in enumerate(entradas):
            # Nombre
            item_nombre = QTableWidgetItem(entrada["nombre"])
            # Formato
            item_formato = QTableWidgetItem(entrada["formato"].upper())
            # Fecha
            item_fecha = QTableWidgetItem(entrada["fecha"])
            # Duración (segundos → mm:ss)
            seg = entrada.get("duracion_seg", 0)
            m, s = divmod(int(seg), 60)
            duracion_str = f"{m:02d}:{s:02d}"
            item_duracion = QTableWidgetItem(duracion_str)

            # Si no existe, tachar y colorear
            if not entrada.get("existe", True):
                for item in [item_nombre, item_formato, item_fecha, item_duracion]:
                    item.setFont(fuente_tachada)
                    item.setForeground(Qt.gray)
                    item.setToolTip("Este archivo ya no existe en la carpeta de grabaciones")

            self.table.setItem(i, 0, item_nombre)
            self.table.setItem(i, 1, item_formato)
            self.table.setItem(i, 2, item_fecha)
            self.table.setItem(i, 3, item_duracion)

    def _limpiar_inexistentes(self):
        """Elimina las entradas cuyos archivos no existen y recarga."""
        if self.history_manager:
            self.history_manager.limpiar_inexistentes()
            self._cargar_datos()