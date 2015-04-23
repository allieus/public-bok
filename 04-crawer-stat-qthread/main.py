import sys
from time import sleep
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from kita import KitaCrawler


class KitaThread(QThread):
    def run(self):
        print('thread start')
        self.result = sum(i for i in range(100000000))
        print('thread end')


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.populate)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.show()

        self.crawer = KitaCrawler()
        self.data = []

    def populate(self):

        self.kita_thread = KitaThread()
        self.kita_thread.finished.connect(self.on_thread_finished)
        self.kita_thread.start()


        '''
        page = self.ui.spinPage.value()
        max = self.ui.spinMax.value()

        rows = self.crawer.get_page(page, max)

        self.ui.tableWidget.setColumnCount(len(self.crawer.header_cols))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.crawer.header_cols)

        self.ui.tableWidget.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(row_idx, col_idx, item)
        '''

    def on_thread_finished(self):
        print('completed')
        print('result : {}'.format(self.kita_thread.result))
        QMessageBox.information(self, '결과', str(self.kita_thread.result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QTableView { selection-color: red; selection-background-color: yellow; }')
    window = Window()
    sys.exit(app.exec_())

