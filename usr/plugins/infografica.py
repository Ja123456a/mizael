import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QMessageBox

class infografica(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Información de la Tarjeta Gráfica')

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 580, 300)
        self.text_edit.setReadOnly(True)

        self.btn_get_info = QPushButton('Obtener Información de la Tarjeta Gráfica', self)
        self.btn_get_info.setGeometry(10, 320, 580, 30)
        self.btn_get_info.clicked.connect(self.get_graphics_card_info)

    def get_graphics_card_info(self):
        command = "lspci | grep VGA"
        result = os.popen(command).read()
        self.text_edit.setPlainText(result)

        # Verificar si la tarjeta gráfica es de AMD o NVIDIA
        if "NVIDIA" in result:
            self.redirect_to_nvidia_page()
        elif "AMD" in result:
            self.redirect_to_amd_page()
        else:
            self.show_error_message()

    def redirect_to_amd_page(self):
        subprocess.Popen(["xdg-open", "https://www.amd.com/es/support"])

    def redirect_to_nvidia_page(self):
        subprocess.Popen(["xdg-open", "https://www.nvidia.es/Download/index.aspx?lang=es"])

    def show_error_message(self):
        QMessageBox.critical(self, "Error", "No se pudo determinar el fabricante de la tarjeta gráfica o estas usando graficos integrados de Intel.")

def main():
    app = QApplication(sys.argv)
    window = infografica()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
