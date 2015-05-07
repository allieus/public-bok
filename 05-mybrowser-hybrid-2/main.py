import os
import sys
import webbrowser
from PyQt5 import uic
from PyQt5.QtCore import QObject, QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWebKitWidgets import QWebPage
from kita import KitaCrawler

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

URLS = [
    ('Hybrid 테스트', 'file://' + os.path.join(ROOT_PATH, 'index.html')),
    ('네이버', 'http://m.naver.com'),
    ('다음', 'http://m.daum.net'),
    ('네이트', 'http://m.nate.com'),
    ('네이버 카페', 'http://m.cafe.naver.com/tmoonworld'),
]


class Hybrid(QObject):
    @pyqtSlot(int, int, result=int)
    def sum(self, x, y):
        return x + y

    @pyqtSlot(int, int, result=str)
    def kita_crawer(self, page, max):
        crawer = KitaCrawler()
        header_cols = crawer.header_cols
        rows = crawer.get_page(page, max)

        thead_content = ''.join('<th>{}</th>'.format(col) for col in header_cols)

        tbody_content = []
        for row in rows:
            tr_content = ''.join('<td>{}</td>'.format(col) for col in row)
            tbody_content.append('<tr>' + tr_content + '</tr>')
        tbody_content = ''.join(tbody_content)

        html = '''
<table>
<thead>{}
</thead>
<tbody>{}
</tbody>
</table>
'''.format(thead_content, tbody_content)

        return html



class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.listWidget.currentRowChanged.connect(self.on_row_changed)
        self.ui.show()

        self.ui.webView.loadFinished.connect(self.on_load_finished)
        self.ui.webView.linkClicked.connect(self.on_link_clicked)

        self.hybrid = Hybrid()
        self.load_data()

    def load_data(self):
        for (name, url) in URLS:
            item = QListWidgetItem(name)
            self.ui.listWidget.addItem(item)

        if URLS:
            self.on_row_changed(0)

    def on_load_finished(self, is_ok):
        if not is_ok:
            self.ui.webView.setHtml('page not found')
        else:
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("hybrid", self.hybrid)
            self.ui.webView.page().setLinkDelegationPolicy(QWebPage.DelegateExternalLinks)

    def on_link_clicked(self, qurl):
        webbrowser.open_new_tab(qurl.url())

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

