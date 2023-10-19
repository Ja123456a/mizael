import sys
import os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QToolBar, QAction, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QMessageBox, QTextBrowser
import zipfile
import rarfile


class CompresorDescompresorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Compresor y Descompresor de Archivos')
        self.setGeometry(100, 100, 800, 600)
        
        self.setStyleSheet("background-color: #021115;")
        self.toolbar = QToolBar()
        self.compress_action = QAction(QIcon(QPixmap('usr/plugins/img/compress.png').scaled(100, 100)), 'Comprimir', self)
        self.compress_action.triggered.connect(self.compressFile)
        self.extract_action = QAction(QIcon(QPixmap('usr/plugins/img/extract.png').scaled(100, 100)), 'Descomprimir', self)
        self.extract_action.triggered.connect(self.extractFile)
        self.test_action = QAction(QIcon(QPixmap('usr/plugins/img/test.png').scaled(100, 100)), 'Testear Archivo', self)
        self.test_action.triggered.connect(self.testFile)
        self.view_action = QAction(QIcon(QPixmap('usr/plugins/img/view.png').scaled(100, 100)), 'Ver Contenido', self)
        self.view_action.triggered.connect(self.viewFile)
        self.info_action = QAction(QIcon(QPixmap('usr/plugins/img/info.png').scaled(100, 100)), 'Información del Archivo', self)
        self.info_action.triggered.connect(self.infoFile)
        self.toolbar.addAction(self.compress_action)
        self.toolbar.addAction(self.extract_action)
        self.toolbar.addAction(self.test_action)
        self.toolbar.addAction(self.view_action)
        self.toolbar.addAction(self.info_action)

        
        self.file_view = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QtCore.QDir.rootPath())
        self.file_view.setModel(self.file_model)
        self.file_view.setRootIndex(
            self.file_model.index(QtCore.QDir.homePath()))
        self.file_view.setColumnWidth(0, 200)
        self.file_view.doubleClicked.connect(self.handleFileDoubleClick)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.file_view)
        self.setLayout(self.layout)

    def handleFileDoubleClick(self, index):
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        if os.path.isfile(file_path):
            self.selected_file = file_path
            self.compress_action.setEnabled(True)
            self.extract_action.setEnabled(True)
            self.test_action.setEnabled(True)
            self.view_action.setEnabled(True)
            self.info_action.setEnabled(True)
        else:
            self.selected_file = None
            self.compress_action.setEnabled(False)
            self.extract_action.setEnabled(False)
            self.test_action.setEnabled(False)
            self.view_action.setEnabled(False)
            self.info_action.setEnabled(False)

    def extractFile(self):
        if self.selected_file:
            if self.selected_file.endswith('.zip'):
                with zipfile.ZipFile(self.selected_file, 'r') as zip_ref:
                    zip_ref.extractall(os.path.dirname(self.selected_file))
                QMessageBox.information(
                    self, 'Extracción Completada', 'Archivo extraído con éxito.')
            elif self.selected_file.endswith('.rar'):
                with rarfile.RarFile(self.selected_file, 'r') as rar_ref:
                    rar_ref.extractall(os.path.dirname(self.selected_file))
                QMessageBox.information(
                    self, 'Extracción Completada', 'Archivo extraído con éxito.')
            else:
                QMessageBox.critical(
                    self, 'Error', 'Formato de archivo no compatible.')

    def testFile(self):
        if self.selected_file:
            if self.selected_file.endswith('.zip'):
                with zipfile.ZipFile(self.selected_file, 'r') as zip_ref:
                    test_result = zip_ref.testzip()
                    if test_result is None:
                        QMessageBox.information(
                            self, 'Test Completado', 'Archivo ZIP válido.')
                    else:
                        QMessageBox.critical(
                            self, 'Test Fallido', f'Error en el archivo ZIP: {test_result}')
            elif self.selected_file.endswith('.rar'):
                with rarfile.RarFile(self.selected_file, 'r') as rar_ref:
                    test_result = rar_ref.testrar()
                    if not test_result:
                        QMessageBox.information(
                            self, 'Test Completado', 'Archivo RAR válido.')
                    else:
                        QMessageBox.critical(
                            self, 'Test Fallido', f'Error en el archivo RAR: {test_result}')
            else:
                QMessageBox.critical(
                    self, 'Error', 'Formato de archivo no compatible.')

    def viewFile(self):
        if self.selected_file:
            try:
                with open(self.selected_file, 'rb') as file:
                    file_content = file.read()
                    hex_content = ' '.join([f'{byte:02X}' for byte in file_content])
                    view_dialog = QTextBrowser()
                    view_dialog.setPlainText(hex_content)
                    view_dialog.setWindowTitle('Contenido del Archivo (Hexadecimal)')
                    view_dialog.show()
            except Exception as e:
                QMessageBox.critical(
                    self, 'Error', f'Error al abrir el archivo: {str(e)}')

    def infoFile(self):
        if self.selected_file:
            file_info = os.stat(self.selected_file)
            info_text = f'Nombre del archivo: {os.path.basename(self.selected_file)}\n'
            info_text += f'Tamaño: {file_info.st_size} bytes\n'
            info_text += f'Fecha de Modificación: {file_info.st_mtime}'
            QMessageBox.information(
                self, 'Información del Archivo', info_text)

    def compressFile(self):
        if self.selected_file:
            compressed_file_name = self.selected_file + '.zip'
            with zipfile.ZipFile(compressed_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                zip_ref.write(self.selected_file,
                              os.path.basename(self.selected_file))
            QMessageBox.information(
                self, 'Compresión Completada', 'Archivo comprimido con éxito en formato ZIP.')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = CompresorDescompresorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
