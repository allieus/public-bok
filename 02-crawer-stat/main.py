import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QTableWidgetItem
)
from kita import KitaCrawler


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

