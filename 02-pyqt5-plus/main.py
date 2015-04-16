import sys
from PyQt5 import uic as pyqt5_uic
# from PyQt4 import uic as pyqt4_uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

STYLESHEET = '''
QWidget#Form {
    background-image: url('python-logo.png');
}
QPushButton {
    background-color: yellow;
}
'''

class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()

        app.setStyleSheet(STYLESHEET)

        self.ui = pyqt5_uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.calc)
        self.ui.show()

    def calc(self):
        a = self.ui.spinA.value()
        b = self.ui.spinB.value()
        result = a + b
        QMessageBox.information(self, '결과', '{} + {} = {}'.format(a, b, result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(app)
    sys.exit(app.exec_())

