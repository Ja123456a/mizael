import sys
import speedtest
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer

class internet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Velocidad de internet")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Presiona el botón para medir tu velocidad de Internet", self)
        self.label.setGeometry(60, 60, 400, 40)

        self.download_label = QLabel("", self)
        self.download_label.setGeometry(50, 100, 300, 30)

        self.upload_label = QLabel("", self)
        self.upload_label.setGeometry(50, 130, 300, 30)

        self.button_measure = QPushButton("Medir Velocidad", self)
        self.button_measure.setGeometry(150, 170, 100, 30)
        self.button_measure.clicked.connect(self.measure_speed)

        self.button_stop = QPushButton("Detener", self)
        self.button_stop.setGeometry(260, 170, 100, 30)
        self.button_stop.clicked.connect(self.stop_measurement)
        self.button_stop.setEnabled(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_speed)

        self.st = None  # Variable para mantener la instancia de speedtest
        self.is_measuring = False

    def measure_speed(self):
        self.is_measuring = True
        self.label.setText("Midiendo velocidad...")
        self.download_label.setText("Velocidad de descarga: Calculando...")
        self.upload_label.setText("Velocidad de subida: Calculando...")

        self.button_measure.setEnabled(False)
        self.button_stop.setEnabled(True)

        self.st = speedtest.Speedtest()
        self.st.get_best_server()
        self.timer.start(2000)  # Actualizar cada 2 segundos

    def stop_measurement(self):
        self.is_measuring = False
        self.timer.stop()
        self.label.setText("Medición detenida")
        self.button_measure.setEnabled(True)
        self.button_stop.setEnabled(False)

    def update_speed(self):
        if self.is_measuring:
            self.st.download()
            self.st.upload()

            download_speed = self.st.results.download / 1_000_000  # Convertir de bits a megabits
            upload_speed = self.st.results.upload / 1_000_000

            self.download_label.setText(f"Velocidad de descarga: {download_speed:.2f} Mbps")
            self.upload_label.setText(f"Velocidad de subida: {upload_speed:.2f} Mbps")

def main():
    app = QApplication(sys.argv)
    window = internet()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
