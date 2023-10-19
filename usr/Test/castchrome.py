from PyQt5 import QtWidgets, QtGui, QtCore
from pychromecast import Chromecast
import pychromecast
from uuid import UUID
import sys

class ChromecastApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Chromecast App')
        self.setGeometry(100, 100, 400, 300)

        self.cast_input = QtWidgets.QLineEdit(self)
        self.cast_input.setPlaceholderText('Nombre del Chromecast (opcional)')
        self.cast_input.setGeometry(10, 10, 380, 30)

        self.uuid_input = QtWidgets.QLineEdit(self)
        self.uuid_input.setPlaceholderText('UUID del Chromecast (opcional)')
        self.uuid_input.setGeometry(10, 50, 380, 30)

        self.search_button = QtWidgets.QPushButton('Buscar Chromecast', self)
        self.search_button.setGeometry(10, 90, 180, 30)
        self.search_button.clicked.connect(self.search_chromecasts)

        self.device_list = QtWidgets.QListWidget(self)
        self.device_list.setGeometry(10, 130, 380, 100)
        self.device_list.itemClicked.connect(self.connect_to_chromecast)

        self.results_text = QtWidgets.QPlainTextEdit(self)
        self.results_text.setGeometry(10, 240, 380, 200)

        self.devices = []  # Lista para almacenar los dispositivos encontrados

    def search_chromecasts(self):
        cast_name = self.cast_input.text()
        cast_uuid = self.uuid_input.text()

        friendly_names = []
        if cast_name:
            friendly_names.append(cast_name)

        uuids = []
        if cast_uuid:
            uuids.append(UUID(cast_uuid))

        devices, browser = pychromecast.discovery.discover_listed_chromecasts(
            friendly_names=friendly_names, uuids=uuids
        )
        # Shut down discovery
        browser.stop_discovery()

        self.devices = devices  # Almacena los dispositivos encontrados en la lista

        result_text = f"Discovered {len(devices)} device(s):\n"
        for device in devices:
            result_text += (
                f"'{device.friendly_name}' ({device.model_name}) @ {device.host}:{device.port} uuid: {device.uuid}\n"
            )
        self.results_text.setPlainText(result_text)

        # Agrega los nombres de los dispositivos a la lista de dispositivos
        self.device_list.clear()
        for device in devices:
            self.device_list.addItem(device.friendly_name)

    def connect_to_chromecast(self, item):
        # Cuando se hace clic en un dispositivo en la lista, intenta conectarse a él
        selected_device_name = item.text()
        selected_device = None

        for device in self.devices:
            if device.friendly_name == selected_device_name:
                selected_device = device
                break

        if selected_device:
            try:
                chromecast = Chromecast('192.168.0.5', 8009)

                chromecast.wait()
                print(f'Conectado a {selected_device.friendly_name}')
                
                # Ahora puedes enviar contenido al Chromecast o realizar otras acciones según tus necesidades
            except Exception as e:
                print(f"No se pudo conectar a {selected_device.friendly_name}: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ChromecastApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
