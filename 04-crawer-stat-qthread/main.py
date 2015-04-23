import sys
from time import sleep
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from kita import KitaCrawler


class KitaThread(QThread):
    status_changed = pyqtSignal(int, str, name='status_changed')

    def __init__(self, page, max):
        super(KitaThread, self).__init__()
        self.page = page
        self.max = max
        self.rows = []
        self.is_running = True

    def run(self):
        self.crawer = KitaCrawler()
        self.header_cols = self.crawer.header_cols

        once = 10

        start_page = self.page
        end_page = self.page + once

        for idx, current_page in enumerate(range(start_page, end_page)):
            if not self.is_running:
                break
            percent = 100 * (idx+1) / (end_page - start_page)

            print('current_page : {}'.format(current_page))
            self.status_changed.emit(percent, '현재 상황 : {}'.format(current_page))
            self.rows.extend(self.crawer.get_page(current_page, self.max))
            sleep(0.1)

    def stop(self):
        self.is_running = False


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.pushButton.clicked.connect(self.on_clicked)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.show()

        self.kita_thread = None

        self.data = []

    def on_clicked(self):
        if self.kita_thread is None:
            self.populate()
        else:
            self.kita_thread.stop()
            self.ui.label.setText('취소되었습니다.')

    def populate(self):
        self.ui.pushButton.setText('취소')

        page = self.ui.spinPage.value()
        max = self.ui.spinMax.value()

        if self.kita_thread is None:
            self.kita_thread = KitaThread(page, max)
            self.kita_thread.status_changed.connect(self.on_thread_status_changed)
            self.kita_thread.finished.connect(self.on_thread_finished)
            self.kita_thread.start()

    def on_thread_status_changed(self, percent, message):
        self.ui.progressBar.setValue(percent)
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
        self.ui.pushButton.setText('시작')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QTableView { selection-color: red; selection-background-color: yellow; }')
    window = Window()
    sys.exit(app.exec_())

