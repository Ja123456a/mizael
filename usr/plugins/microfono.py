import subprocess
import sys
import time
from PyQt5 import QtWidgets

# Nombre del micrófono virtual
virtual_mic_name = "Microfono_Virtual"


class MicrofonoVirtual(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.start_button = QtWidgets.QPushButton('Iniciar')
        self.stop_button = QtWidgets.QPushButton('Detener')
        self.status_label = QtWidgets.QLabel('Micrófono Virtual: No creado')

        # Agregar un campo para seleccionar la fuente de señal
        self.signal_source_label = QtWidgets.QLabel('Fuente de señal:')
        self.signal_source_combo = QtWidgets.QComboBox()
        self.signal_source_combo.addItem('USB')
        self.signal_source_combo.addItem('Wi-Fi (IP)')

        # Campo para ingresar la dirección IP (visible cuando se selecciona Wi-Fi)
        self.ip_label = QtWidgets.QLabel('Dirección IP:Puerto')
        self.ip_input = QtWidgets.QLineEdit()
        self.ip_label.setVisible(False)
        self.ip_input.setVisible(False)

        self.start_button.clicked.connect(self.create_virtual_microphone)
        self.stop_button.clicked.connect(self.remove_virtual_microphone)

        # Conectar la selección de fuente de señal al cambio de visibilidad del campo de dirección IP
        self.signal_source_combo.currentIndexChanged.connect(
            self.toggle_ip_input)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.signal_source_label)
        layout.addWidget(self.signal_source_combo)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.setWindowTitle('Micrófono Virtual')
        self.setGeometry(100, 100, 300, 200)

        self.audio_process = None

    def toggle_ip_input(self, index):
        # Mostrar u ocultar el campo de dirección IP según la selección de fuente de señal
        if index == 0:  # USB seleccionado
            self.ip_label.setVisible(False)
            self.ip_input.setVisible(False)
        else:  # Wi-Fi (IP) seleccionado
            self.ip_label.setVisible(True)
            self.ip_input.setVisible(True)

    def create_virtual_microphone(self):
        signal_source = self.signal_source_combo.currentText()

        # Si la fuente de señal es Wi-Fi (IP), obtén la dirección IP ingresada
        if signal_source == 'Wi-Fi (IP)':
            ip = self.ip_input.text()
            # Verifica si la dirección IP es válida antes de crear el micrófono virtual
            if not self.is_valid_ip(ip):
                QtWidgets.QMessageBox.warning(
                    self, 'Advertencia', 'Dirección IP no válida.')
                return
        else:
            ip = None

        # Lógica para crear el micrófono virtual según la fuente de señal seleccionada
        if signal_source == 'USB':
            # Agregar la lógica para la fuente USB aquí
            pass
        elif signal_source == 'Wi-Fi (IP)':
            # Agregar la lógica para la fuente Wi-Fi (IP) aquí
            pass

    def create_virtual_microphone(self):
        command = [
            'pactl',
            'load-module',
            'module-pipe-source',
            'source_name=' + virtual_mic_name,
            'file=/tmp/virtual_mic',
        ]
        subprocess.run(command)
        self.status_label.setText('Micrófono Virtual: Creado')

    def remove_virtual_microphone(self):
        command = [
            'pactl',
            'unload-module',
            'module-pipe-source',
        ]
        subprocess.run(command)
        self.status_label.setText('Micrófono Virtual: Eliminado')


def is_valid_ip(self, ip):
    return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MicrofonoVirtual()
    window.show()
    sys.exit(app.exec_())
