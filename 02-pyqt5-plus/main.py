import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.calc)
        self.ui.show()

    def calc(self):
        a = self.ui.spinA.value()
        b = self.ui.spinB.value()
        result = a + b
        QMessageBox.information(self, '결과', '{} + {} = {}'.format(a, b, result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

