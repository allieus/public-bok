import sys
from time import sleep
from PyQt5 import uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from kita import KitaCrawler


class KitaThread(QThread):
    def __init__(self, page, max):
        super(KitaThread, self).__init__()
        self.page = page
        self.max = max

    def run(self):
        self.crawer = KitaCrawler()

        self.header_cols = self.crawer.header_cols
        self.rows = self.crawer.get_page(self.page, self.max)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.populate)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.show()

        self.data = []

    def populate(self):
        page = self.ui.spinPage.value()
        max = self.ui.spinMax.value()

        self.kita_thread = KitaThread(page, max)
        self.kita_thread.finished.connect(self.on_thread_finished)
        self.kita_thread.start()

    def on_thread_finished(self):
        self.ui.tableWidget.setColumnCount(len(self.kita_thread.header_cols))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.kita_thread.header_cols)

        self.ui.tableWidget.setRowCount(len(self.kita_thread.rows))
        for row_idx, row in enumerate(self.kita_thread.rows):
            for col_idx, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(row_idx, col_idx, item)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QTableView { selection-color: red; selection-background-color: yellow; }')
    window = Window()
    sys.exit(app.exec_())

