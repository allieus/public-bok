import sys
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem

URLS = [
    ('네이버', 'http://m.naver.com'),
    ('다음', 'http://m.daum.net'),
    ('네이트', 'http://m.nate.com'),
]

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.listWidget.currentRowChanged.connect(self.on_row_changed)
        self.ui.show()

        self.load_data()

    def load_data(self):
        for (name, url) in URLS:
            item = QListWidgetItem(name)
            self.ui.listWidget.addItem(item)

        if URLS:
            self.on_row_changed(0)

    def on_row_changed(self, current_row):
        name, url = URLS[current_row]
        self.ui.webView.load(QUrl(url))

def load_stylesheet():
    return open('main.css', 'rb').read().decode('utf8')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = Window()
    sys.exit(app.exec_())
