from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
)


class DialogoGuardar(QDialog):
    """Pide al usuario el nombre con el que quiere guardar la grabación."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guardar")
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Nombre del archivo:"))

        self.edit = QLineEdit("grabacion")
        self.edit.selectAll()
        layout.addWidget(self.edit)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    @property
    def nombre(self) -> str:
        return self.edit.text().strip() or "grabacion"