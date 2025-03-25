import gi
import os
from threading import Thread
from puzzle1 import Rfid  # Importa la classe Rfid del mòdul puzzle1

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

class NFCReaderApp:
    def __init__(self):
        # Configuració inicial de la finestra de l'aplicació
        self.window = Gtk.Window(title="Lectura de targeta NFC")
        self.window.set_default_size(350, 200)  # Dimensions de la finestra
        self.window.connect("destroy", self.stop)

        # Contenidor per als elements de la interfície
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.window.add(self.box)

        # Etiqueta on es mostraran els missatges al usuari
        self.label = Gtk.Label(label="Passi la seva targeta NFC")
        self.label.set_margin_top(8)
        self.label.set_margin_bottom(2)
        self.label.set_margin_start(8)
        self.label.set_margin_end(8)
        self.label.get_style_context().add_class("nfc-label")  # Aplica estils CSS

        self.box.pack_start(self.label, True, True, 0)

        # Botó per netejar la informació mostrada a l'etiqueta
        self.clear_button = Gtk.Button(label="Netejar")
        self.clear_button.set_margin_top(2)
        self.clear_button.set_margin_bottom(5)
        self.clear_button.set_margin_start(8)
        self.clear_button.set_margin_end(8)
        self.clear_button.get_style_context().add_class("nfc-button")
        self.clear_button.connect("clicked", self.clear_label)
        self.box.pack_start(self.clear_button, False, False, 0)

        # Inicialització del lector NFC
        self.rfid = Rfid()

        # Carrega els estils CSS des d'un fitxer extern
        self.apply_css()

        # Configura i inicia el fil per llegir targetes NFC
        self.running = True
        self.nfc_thread = Thread(target=self.read_nfc, daemon=True)
        self.nfc_thread.start()

        self.window.show_all()

    def apply_css(self):
        """Carrega el CSS des d'un fitxer extern 'uinfc.css'."""
        css_path = os.path.join(os.path.dirname(__file__), "uinfc.css")
        style_provider = Gtk.CssProvider()

        try:
            with open(css_path, "rb") as css_file:
                style_provider.load_from_data(css_file.read())
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            print("CSS carregat correctament des de 'uinfc.css'.")
        except Exception as e:
            print(f"No s'ha pogut carregar el CSS: {e}")

    def read_nfc(self):
        """Bucle per llegir targetes NFC mentre l'aplicació estigui activa."""
        while self.running:
            try:
                uid = self.rfid.read_uid()
                if uid:
                    print(f"UID llegit: {uid}")
                    GLib.idle_add(self.update_label, uid)
            except Exception as e:
                print(f"Error en llegir NFC: {e}")

    def update_label(self, uid):
        """Actualitza l'etiqueta amb el UID llegit i canvia el color de fons a verd."""
        self.label.set_text(f"UID: {uid}")
        self.label.get_style_context().remove_class("nfc-label")
        self.label.get_style_context().add_class("nfc-label-green")

    def clear_label(self, button):
        """Neteja l'etiqueta i la prepara per una nova lectura."""
        self.label.set_text("Passi la seva targeta NFC")
        self.label.get_style_context().remove_class("nfc-label-green")
        self.label.get_style_context().add_class("nfc-label")

    def stop(self, *args):
        """Atura el procés de lectura de NFC i tanca l'aplicació correctament."""
        self.running = False
        self.rfid.close()
        Gtk.main_quit()

# Inicia l'aplicació
app = NFCReaderApp()
Gtk.main()