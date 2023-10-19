import sys
import subprocess
import requests
import os
from PyQt5 import QtWidgets, QtGui, QtCore


class navegadores(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Instalador de Navegadores')
        self.setGeometry(100, 100, 400, 200)

        # Layout vertical para los widgets
        layout = QtWidgets.QVBoxLayout()

        # Agregar una imagen encima del botón de Chrome
        chrome_image_label = QtWidgets.QLabel(self)
        chrome_image = QtGui.QPixmap('usr/plugins/img/chrome.png').scaled(240, 120)  # Escalar la imagen a 64x64 píxeles
        chrome_image_label.setPixmap(chrome_image)

        self.chrome_button = QtWidgets.QPushButton('Descargar e Instalar Chrome', self)
        self.chrome_button.clicked.connect(self.install_chrome)

        layout.addWidget(chrome_image_label, alignment=QtCore.Qt.AlignHCenter)  # Centrar la imagen horizontalmente
        layout.addWidget(self.chrome_button, alignment=QtCore.Qt.AlignHCenter)  # Centrar el botón horizontalmente

        # Agregar una imagen encima del botón de Opera
        opera_image_label = QtWidgets.QLabel(self)
        opera_image = QtGui.QPixmap('usr/plugins/img/opera.png').scaled(240, 120)  # Escalar la imagen a 64x64 píxeles
        opera_image_label.setPixmap(opera_image)

        self.opera_button = QtWidgets.QPushButton('Descargar e Instalar Opera', self)
        self.opera_button.clicked.connect(self.install_opera)

        layout.addWidget(opera_image_label, alignment=QtCore.Qt.AlignHCenter)  # Centrar la imagen horizontalmente
        layout.addWidget(self.opera_button, alignment=QtCore.Qt.AlignHCenter)  # Centrar el botón horizontalmente

        self.setLayout(layout)  # Establecer el diseño como el diseño principal


    def install_chrome(self):
        chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        download_path = "/tmp/chrome.deb"
        
        # Descargar el archivo .deb de Chrome
        response = requests.get(chrome_url)
        with open(download_path, 'wb') as f:
            f.write(response.content)

        # Instalar Chrome usando dpkg
        try:
            subprocess.check_output(["sudo", "dpkg", "-i", download_path])
            subprocess.check_output(["sudo", "apt-get", "install", "-f"])  # Para resolver las dependencias
            os.remove(download_path)  # Eliminar el archivo .deb después de la instalación
            QtWidgets.QMessageBox.information(self, "Éxito", "Google Chrome se ha instalado correctamente.")
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al instalar Chrome: {e.output.decode()}")

    def install_opera(self):
        opera_url = "https://download3.operacdn.com/ftp/pub/opera/desktop/102.0.4880.46/linux/opera-stable_102.0.4880.46_amd64.deb"
        download_path = "/tmp/opera.deb"
        
        # Descargar el archivo .deb de Opera
        response = requests.get(opera_url)
        with open(download_path, 'wb') as f:
            f.write(response.content)

        # Instalar Opera usando dpkg
        try:
            subprocess.check_output(["sudo", "dpkg", "-i", download_path])
            subprocess.check_output(["sudo", "apt-get", "install", "-f"])  # Para resolver las dependencias
            os.remove(download_path)  # Eliminar el archivo .deb después de la instalación
            QtWidgets.QMessageBox.information(self, "Éxito", "Opera se ha instalado correctamente.")
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al instalar Opera: {e.output.decode()}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = navegadores()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
