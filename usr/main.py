import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import subprocess


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Botón para lanzar el micrófono
        self.launch_microfono_button = self.create_button('usr/img/microfono.png', 'Micrófono Virtual', self.launch_microfono)

        # Botón para probar la red
        self.test_net_button = self.create_button('usr/img/internet.png', 'Test de Velocidad', self.launch_internet)

        # Botón para ejecutar "infografica.py"
        self.infografica_button = self.create_button('usr/img/infografica.png', 'Información Grafica', self.launch_infografica)

        # Botón para ejecutar "navegador.py"
        self.navegadores_button = self.create_button('usr/img/navegadores.png', 'Descargar Navegadores', self.launch_navegadores)
        
        # Botón para ejecutar "zip_rar.py"
        self.ziprar_button = self.create_button('usr/img/zip_rar.png', 'LinuxRAR', self.launch_ziprar)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.launch_microfono_button)
        layout.addWidget(self.test_net_button)
        layout.addWidget(self.infografica_button)
        layout.addWidget(self.navegadores_button)
        layout.addWidget(self.ziprar_button)
        self.setLayout(layout)

        self.setWindowTitle('Plugins Andy')
        self.setGeometry(150, 150, 250, 300)

    def create_button(self, icon_path, text, slot):
        button = QtWidgets.QPushButton()
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(64, 64))
        button.clicked.connect(slot)

        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(label)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        return widget

    def launch_microfono(self):
        try:
            # Obtiene la ruta completa al archivo "microfono.py" en la carpeta "plugins"
            microfono_path = os.path.join(os.path.dirname(
                __file__), 'plugins', 'microfono.py')
            subprocess.run(['python3', microfono_path])
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'El archivo "microfono.py" no se encontró.')

    def launch_internet(self):
        try:
            # Obtiene la ruta completa al archivo "internet.py" en la carpeta "plugins"
            internet_path = os.path.join(os.path.dirname(
                __file__), 'plugins', 'internet.py')
            subprocess.run(['python3', internet_path])
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'El archivo "internet.py" no se encontró.')

    def launch_infografica(self):
        try:
            # Obtiene la ruta completa al archivo "infografica.py" en la carpeta "plugins"
            infografica_path = os.path.join(os.path.dirname(
                __file__), 'plugins', 'infografica.py')
            subprocess.run(['python3', infografica_path])
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'El archivo "infografica.py" no se encontró.')

    def launch_navegadores(self):
        try:
            # Obtiene la ruta completa al archivo "navegadores.py" en la carpeta "plugins"
            navegadores_path = os.path.join(os.path.dirname(
                __file__), 'plugins', 'navegadores.py')
            subprocess.run(['python3', navegadores_path])
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'El archivo "navegadores.py" no se encontró.')

    def launch_ziprar(self):
        try:
            # Obtiene la ruta completa al archivo "ziprar.py" en la carpeta "plugins"
            ziprar_path = os.path.join(os.path.dirname(
                __file__), 'plugins', 'ziprar.py')
            subprocess.run(['python3', ziprar_path])
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self, 'Advertencia', 'El archivo "ziprar.py" no se encontró.')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    launcher = Main()
    launcher.show()
    sys.exit(app.exec_())
