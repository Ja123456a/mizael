import cv2
import numpy as np
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton

class Image3DApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Detección de Movimiento")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)

        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Introduce la dirección IP del video")
        self.layout.addWidget(self.ip_input)

        self.start_button = QPushButton("Iniciar Detección", self)
        self.start_button.clicked.connect(self.start_detection)
        self.layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.layout)

        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_detection_started = False

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def start_detection(self):
        if not self.is_detection_started:
            ip_address = self.ip_input.text()
            if not ip_address:
                return

            self.capture = cv2.VideoCapture(ip_address)
            self.timer.start(30)
            self.is_detection_started = True
            self.start_button.setText("Detener Detección")
        else:
            self.capture.release()
            self.timer.stop()
            self.image_label.clear()
            self.is_detection_started = False
            self.start_button.setText("Iniciar Detección")

    def update_frame(self):
        ret, frame = self.capture.read()

        if ret:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            # Realiza la detección de personas y resalta en rojo
            frame = self.detect_and_highlight_movement(frame)

            h, w, _ = frame.shape
            bytes_per_line = 3 * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(q_pixmap)

    def detect_and_highlight_movement(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        human_rects, _ = self.hog.detectMultiScale(
            gray,
            winStride=(8, 8),  
            padding=(16, 16), 
            scale=1.05
        )

        for (x, y, w, h) in human_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Image3DApp()
    window.show()
    sys.exit(app.exec_())
