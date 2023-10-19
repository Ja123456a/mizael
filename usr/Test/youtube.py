import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://accounts.google.com/InteractiveLogin/signinchooser?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Des-419%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&ec=65620&hl=es-419&passive=true&service=youtube&uilel=3&ifkv=AYZoVhel_y6lqrxJbfsHhids_9V1qmjsNg-5GhNx5ylQ0WbeZn_zxfLuKs1iasbIPuIlCyu1sy7t-Q&theme=glif&flowName=GlifWebSignIn&flowEntry=ServiceLogin"))
        self.setWindowTitle("Youtube")
        self.setCentralWidget(self.browser)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.showMaximized()
    sys.exit(app.exec_())#eso es todo bro XD