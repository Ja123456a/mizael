import cv2
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QFormLayout, QVBoxLayout

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.camera_urls = []  # Lista de URL de cámaras
        self.video_captures = []  # Lista de objetos de captura de video
        self.current_camera_index = 0

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Iniciar Detección", self)
        self.start_button.clicked.connect(self.start_detection)

        self.camera_url_input = QLineEdit(self)
        self.add_camera_button = QPushButton("Agregar Cámara", self)
        self.add_camera_button.clicked.connect(self.add_camera)

        self.camera_layout = QVBoxLayout()
        self.camera_layout.addWidget(self.video_label)
        self.camera_layout.addWidget(self.start_button)

        self.camera_control_layout = QFormLayout()
        self.camera_control_layout.addRow("URL de la Cámara:", self.camera_url_input)
        self.camera_control_layout.addRow(self.add_camera_button)

        self.layout = QHBoxLayout(self.central_widget)
        self.layout.addLayout(self.camera_layout)
        self.layout.addLayout(self.camera_control_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_detecting = False

    def add_camera(self):
        camera_url = self.camera_url_input.text()
        if camera_url:
            self.camera_urls.append(camera_url)
            self.video_captures.append(cv2.VideoCapture(camera_url))
            self.camera_url_input.clear()

    def start_detection(self):
        if not self.is_detecting:
            self.is_detecting = True
            self.start_button.setText("Detener Detección")
            self.timer.start(100)  # Actualiza el marco cada 100 ms
        else:
            self.is_detecting = False
            self.start_button.setText("Iniciar Detección")
            self.timer.stop()

    def update_frame(self):
        if not self.video_captures:
            return

        ret, frame = self.video_captures[self.current_camera_index].read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        for capture in self.video_captures:
            capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceDetectionApp()
    window.setWindowTitle("Detección de Caras con Múltiples Cámaras")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
