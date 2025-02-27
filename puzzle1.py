import nfc  # Importa la librería nfcpy para interactuar con dispositivos NFC.

class Rfid:
    def __init__(self):
        self.clf = nfc.ContactlessFrontend('usb')
        self.tag = None  # Variable para almacenar el tag detectado
    
    def on_connect(self, tag):
        self.tag = tag  # Guarda el objeto tag
        return True  # Permite que continue el proceso de lectura

    def read_uid(self):
        try:
            print("Esperando tarjeta NFC...")
            self.clf.connect(rdwr={'on-connect': self.on_connect})  # Usa una función real, no lambda
            if self.tag:
                return self.tag.identifier.hex()  # Devuelve el UID en formato hexadecimal
            return None
        except Exception as e:
            print(f"Error al leer UID: {e}")
            return None
    
    def close(self):
        self.clf.close()

if __name__ == "__main__":
    rf = Rfid()
    uid = rf.read_uid()
    if uid:
        print(f"UID de la tarjeta: {uid}")
    rf.close()
