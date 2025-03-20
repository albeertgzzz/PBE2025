import gi
from threading import Thread
from puzzle1 import Rfid  # Importa la classe Rfid del puzzle 1

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class NFCReaderApp:
    def __init__(self):
        self.window = Gtk.Window(title="Lectura de targeta NFC")
        self.window.set_default_size(300, 150)
        self.window.connect("destroy", self.stop)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.window.add(self.box)

        # Etiqueta per mostrar el missatge
        self.label = Gtk.Label(label="Passi la seva targeta NFC")
        self.label.set_markup('<span foreground="blue" size="large">Passi la seva targeta NFC</span>')
        self.box.pack_start(self.label, True, True, 0)

        # Botó per esborrar el missatge
        self.clear_button = Gtk.Button(label="Netejar")
        self.clear_button.connect("clicked", self.clear_label)
        self.box.pack_start(self.clear_button, True, True, 0)

        # Inicialitzar el lector NFC
        self.rfid = Rfid()

        # Llançar el fil per llegir NFC
        self.running = True
        self.nfc_thread = Thread(target=self.read_nfc, daemon=True)
        self.nfc_thread.start()

        self.window.show_all()

    def read_nfc(self):
        """Llegeix l'UID una sola vegada i atura el procés."""
        try:
            uid = self.rfid.read_uid()
            if uid:
                GLib.idle_add(self.update_label, uid)
                self.running = False  # Aturar el fil després de llegir una targeta
                self.rfid.close()
        except Exception as e:
            print(f"Error al llegir NFC: {e}")

    def update_label(self, uid):
        """Actualitza la interfície amb l'UID llegit."""
        self.label.set_markup(f'<span foreground="red" size="large">uid: {uid}</span>')

    def clear_label(self, button):
        """Neteja el missatge de la interfície."""
        self.label.set_markup('<span foreground="blue" size="large">Passi la seva targeta NFC</span>')

    def stop(self, *args):
        """Atura el fil del lector NFC i tanca la finestra."""
        self.running = False
        self.rfid.close()
        Gtk.main_quit()

# Llança l'aplicació
app = NFCReaderApp()
Gtk.main()
