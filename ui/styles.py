TEMAS = {
    "oscuro": {"bg": "#1e1e1e", "fg": "#ffffff", "btn": "#333333", "brd": "#444444"},
    "claro":  {"bg": "#f0f0f0", "fg": "#222222", "btn": "#ffffff", "brd": "#cccccc"},
}


def obtener_estilo(t: dict) -> str:
    return f"""
        QWidget {{ background-color: {t['bg']}; color: {t['fg']}; font-family: "DejaVu Sans"; }}
        QLabel#reloj {{ font-size: 40px; font-weight: 200; margin: 6px 0; letter-spacing: 2px; }}
        QLabel#estado {{ font-size: 11px; font-weight: bold; }}
        QPushButton {{
            background-color: {t['btn']}; border: 1px solid {t['brd']};
            border-radius: 4px; padding: 8px; color: {t['fg']};
        }}
        QPushButton:disabled {{ color: #777777; background-color: {t['bg']}; }}
        QPushButton#btn_tema {{ font-size: 20px; background: transparent; border: none; color: {t['fg']}; }}
        QComboBox, QLineEdit {{ background-color: {t['btn']}; border: 1px solid {t['brd']}; color: {t['fg']}; padding: 4px; }}
    """