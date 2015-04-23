import sys
from time import sleep
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from kita import KitaCrawler


class KitaThread(QThread):
    status_changed = pyqtSignal(str, name='status_changed')

    def __init__(self, page, max):
        super(KitaThread, self).__init__()
        self.page = page
        self.max = max
        self.rows = []

    def run(self):
        self.crawer = KitaCrawler()
        self.header_cols = self.crawer.header_cols

        once = 10

        start_page = self.page
        end_page = self.page + once

        for current_page in range(start_page, end_page):
            print('current_page : {}'.format(current_page))
            self.status_changed.emit('현재 상황 : {}'.format(current_page))
            self.rows.extend(self.crawer.get_page(current_page, self.max))
            sleep(0.1)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.populate)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.show()

        self.kita_thread = None

        self.data = []

    def populate(self):
        page = self.ui.spinPage.value()
        max = self.ui.spinMax.value()

        if self.kita_thread is None:
            self.kita_thread = KitaThread(page, max)
            self.kita_thread.status_changed.connect(self.on_thread_status_changed)
            self.kita_thread.finished.connect(self.on_thread_finished)
            self.kita_thread.start()

    def on_thread_status_changed(self, message):
        self.ui.label.setText(message)

    def on_thread_finished(self):
        self.ui.tableWidget.setColumnCount(len(self.kita_thread.header_cols))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.kita_thread.header_cols)

        self.ui.tableWidget.setRowCount(len(self.kita_thread.rows))
        for row_idx, row in enumerate(self.kita_thread.rows):
            for col_idx, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(row_idx, col_idx, item)

        self.kita_thread = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QTableView { selection-color: red; selection-background-color: yellow; }')
    window = Window()
    sys.exit(app.exec_())

