import sys
import asyncio
from PyQt5 import QtWidgets, QtGui, QtCore
import pyatv

class AppleTVScanner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Escáner de Apple TV con PyQt5')
        self.setGeometry(100, 100, 400, 400)

        self.result_label = QtWidgets.QLabel(self)
        self.result_label.setGeometry(10, 10, 380, 280)
        self.result_label.setAlignment(QtCore.Qt.AlignTop)

        self.scan_button = QtWidgets.QPushButton('Buscar Dispositivos AirPlay', self)
        self.scan_button.setGeometry(10, 310, 180, 30)
        self.scan_button.clicked.connect(self.scan_and_display)

    async def get_active_devices(self):
        """Find active AirPlay devices."""
        atvs = await pyatv.scan(asyncio.get_event_loop(), timeout=5)

        active_devices = []

        for atv in atvs:
            if atv.get_service("airplay"):
                active_devices.append(atv)

        return active_devices

    async def scan_and_display(self):
        self.scan_button.setEnabled(False)  # Deshabilita el botón mientras escanea
        self.result_label.setText("Buscando dispositivos AirPlay...")

        active_devices = await self.get_active_devices()

        if not active_devices:
            info = "No se encontraron dispositivos AirPlay activos."
        else:
            info = "Dispositivos AirPlay activos:\n"
            for device in active_devices:
                info += f"- Nombre: {device.name}, Dirección IP: {device.address}\n"

        self.result_label.setText(info)
        self.scan_button.setEnabled(True)  # Habilita nuevamente el botón después de escanear

def main():
    app = QtWidgets.QApplication(sys.argv)
    scanner = AppleTVScanner()
    scanner.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
