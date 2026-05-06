import os
import json
from datetime import datetime
import soundfile as sf


class HistoryManager:
    """Gestiona el historial de grabaciones en un archivo JSON."""

    def __init__(self):
        # Carpeta oculta en el home del usuario
        self.config_dir = os.path.join(os.path.expanduser("~"), ".bico")
        os.makedirs(self.config_dir, exist_ok=True)
        self.json_path = os.path.join(self.config_dir, "historial.json")
        if not os.path.exists(self.json_path):
            self._write([])

    def _read(self):
        """Lee el historial desde el archivo JSON."""
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, data):
        """Escribe la lista de entradas en el JSON."""
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, ruta_archivo, formato):
        """
        Añade una nueva entrada al historial.
        Calcula la duración con soundfile.
        """
        if not os.path.exists(ruta_archivo):
            return

        try:
            info = sf.info(ruta_archivo)
            duracion = info.duration  # en segundos
        except Exception:
            duracion = 0

        nombre = os.path.basename(ruta_archivo)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entrada = {
            "nombre": nombre,
            "formato": formato,
            "fecha": fecha,
            "duracion_seg": round(duracion, 1),
            "ruta": ruta_archivo
        }

        data = self._read()
        data.append(entrada)
        self._write(data)

    def listar(self):
        """Devuelve la lista de entradas con verificación de existencia."""
        data = self._read()
        for entrada in data:
            entrada["existe"] = os.path.exists(entrada["ruta"])
        return data

    def limpiar_inexistentes(self):
        """Elimina del historial las entradas cuyos archivos no existen."""
        data = self._read()
        data = [e for e in data if os.path.exists(e["ruta"])]
        self._write(data)