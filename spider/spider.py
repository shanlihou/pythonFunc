#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
# from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import (QWidget, QPushButton, QGridLayout, QComboBox, QScrollArea,
                             QCheckBox, QLabel, QVBoxLayout, QApplication)
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
# from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont


class CallHandler(QObject):
    def __init__(self, browser):
        super(CallHandler, self).__init__()
        self._browser = browser

    @pyqtSlot(result=str)
    def init(self):
        print('im in browser init')
        self._browser.initFocus()
        return 'browser'

    @pyqtSlot(result=str)
    def myHello(self):
        print('im in hello')
        # view.page().runJavaScript('uptext("hello, Python");')
        print('call received')
        return 'hello, Python'

    @pyqtSlot(str, result=str)
    def myTest(self, test):
        return test
    
class Spider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initBrowser(self):
        view = QWebEngineView()
        channel = QWebChannel()
        handler = CallHandler(self)
        channel.registerObject('pyjs', handler)
        view.page().setWebChannel(channel)
        url_string = "http://javbest.net/category/uncensored/page/1/"
        view.load(QUrl(url_string))
        view.show()
        self.view = view
        self.channel = channel
        self.handler = handler
        
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        self.initBrowser()
        grid.addWidget(self.view, 3, 0, 3, 4)
        self.setLayout(grid)
        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('BuriedLove')
        self.show()
        
        
    def test(self):
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sp = Spider()
    sys.exit(app.exec_())
    