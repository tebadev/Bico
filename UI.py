import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from modules.recorder import AudioUtilidades, inicializador

class BicoApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Grabadora")
        self.set_default_size(320, 400)
        self.set_resizable(False)
        self.set_border_width(20)

        # Estado
        self.motor, self.grabando, self.pausado, self.segundos = None, False, False, 0
        self.oscuro = False
        self.micros = list(AudioUtilidades.detectar_microfonos())

        # Estilo
        self.provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), self.provider, 600)

        self.UI()
        self.set_tema()
        self.show_all()

    def set_tema(self, *args):
        self.oscuro = not self.oscuro
        # Colores: [Fondo, Texto, Boton, Borde, IconoColor]
        c = ["#1e1e1e", "#fff", "#2d2d2d", "#3d3d3d", "#fff"] if self.oscuro else ["#f2f2f2", "#222", "#fff", "#ddd", "#000"]
        self.btn_tema.set_label("☀️" if self.oscuro else "🌙")
        
        css = f"""
        window {{ background: {c[0]}; }}
        label {{ color: {c[1]}; }}
        #reloj {{ font-size: 60px; font-weight: 200; margin: 10px 0; }}
        #estado {{ font-size: 11px; opacity: 0.5; }}
        button {{ background: {c[2]}; border: 1px solid {c[3]}; color: {c[1]}; border-radius: 4px; padding: 8px; }}
        combobox {{ background: {c[2]}; border: 1px solid {c[3]}; }}
        #btn-t {{ background: none; border: none; font-size: 20px; color: {c[4]}; }}
        """
        self.provider.load_from_data(css.encode())

    def UI(self):
        v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(v)

        # Header Tema
        h = Gtk.Box()
        self.btn_tema = Gtk.Button()
        self.btn_tema.set_name("btn-t")
        self.btn_tema.connect("clicked", self.set_tema)
        h.pack_end(self.btn_tema, False, False, 0)
        v.pack_start(h, False, False, 0)

        # Reloj
        self.lbl_t = Gtk.Label(label="00:00", name="reloj")
        self.lbl_e = Gtk.Label(label="Listo", name="estado")
        v.pack_start(self.lbl_t, False, False, 0)
        v.pack_start(self.lbl_e, False, False, 0)

        # Selectores
        self.cb_mic = Gtk.ComboBoxText()
        self.cb_mic.append_text("Micrófono por defecto")
        [self.cb_mic.append_text(m[1]) for m in self.micros]
        self.cb_mic.set_active(0)

        self.cb_fmt = Gtk.ComboBoxText()
        [self.cb_fmt.append_text(f) for f in ["WAV", "MP3", "FLAC", "OGG"]]
        self.cb_fmt.set_active(0)

        for w in [Gtk.Label(label="Entrada:"), self.cb_mic, Gtk.Label(label="Formato:"), self.cb_fmt]:
            v.pack_start(w, False, False, 0)

        # Botones
        btns = Gtk.Box(spacing=10, homogeneous=True)
        self.b_rec = Gtk.Button(label="Grabar")
        self.b_pau = Gtk.Button(label="Pausar", sensitive=False)
        self.b_stp = Gtk.Button(label="Parar", sensitive=False)
        
        self.b_rec.connect("clicked", self.on_rec)
        self.b_pau.connect("clicked", self.on_pau)
        self.b_stp.connect("clicked", self.on_stp)

        [btns.pack_start(b, True, True, 0) for b in [self.b_rec, self.b_pau, self.b_stp]]
        v.pack_start(btns, False, False, 10)

    def tick(self):
        if not self.grabando: return False
        if not self.pausado:
            self.segundos += 1
            self.lbl_t.set_text(f"{self.segundos//60:02d}:{self.segundos%60:02d}")
        return True

    def on_rec(self, _):
        idx = self.cb_mic.get_active()
        mid = None if idx == 0 else self.micros[idx-1][0]
        self.motor = inicializador(44100, 1, mid)
        self.grabando, self.pausado, self.segundos = True, False, 0
        self.lbl_e.set_text("Grabando...")
        self.toggle_btns(False)
        GLib.timeout_add(1000, self.tick)

    def on_pau(self, _):
        self.pausado = not self.pausado
        self.motor.pausar() if self.pausado else self.motor.reanudar()
        self.b_pau.set_label("Reanudar" if self.pausado else "Pausar")
        self.lbl_e.set_text("Pausado" if self.pausado else "Grabando...")

    def on_stp(self, _):
        self.motor.detener()
        self.grabando = False
        tmp = self.motor.archivo_temporal
        if tmp: self.save(tmp)
        self.lbl_t.set_text("00:00")
        self.lbl_e.set_text("Listo")
        self.toggle_btns(True)

    def toggle_btns(self, st):
        self.b_rec.set_sensitive(st)
        self.cb_mic.set_sensitive(st)
        self.cb_fmt.set_sensitive(st)
        self.b_pau.set_sensitive(not st)
        self.b_stp.set_sensitive(not st)

    def save(self, tmp):
        fmt = self.cb_fmt.get_active_text().lower()
        d = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Guardar archivo")
        d.format_secondary_text(f"Nombre del archivo (.{fmt}):")
        en = Gtk.Entry(text="grabacion")
        d.get_content_area().pack_end(en, False, False, 10)
        d.show_all()
        if d.run() == Gtk.ResponseType.OK:
            AudioUtilidades.guardar_archivo(tmp, "grabaciones", en.get_text(), fmt)
        d.destroy()

if __name__ == "__main__":
    app = BicoApp()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()