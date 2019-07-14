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


class Browser(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initBrowser(self):
        view = QWebEngineView()
        channel = QWebChannel()
        handler = CallHandler(self)
        channel.registerObject('pyjs', handler)
        view.page().setWebChannel(channel)
        url_string = "https://bing.com"
        view.load(QUrl(url_string))
        view.show()
        self.view = view
        self.channel = channel
        self.handler = handler

    def initFocus(self):
        self.setPos(self._posStr)

    def test(self):
        print('im in browser test')

    def createComBox(self, texts):
        # combox
        combo = QComboBox(self)
        for text in texts:
            combo.addItem(text)

        def changeTopic(slot):
            self._topic = slot

        combo.activated[str].connect(changeTopic)
        return combo

    def createDevCombox(self):
        combo = QComboBox(self)
        self.devComb = combo

        def changeDevId(devId):
            self._devId = devId

        combo.activated[str].connect(changeDevId)
        return combo

    def runJs(self, jsStr):
        self.view.page().runJavaScript(jsStr)

    def createButton(self, name, func):
        btn = QPushButton(name, self)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(func)
        return btn

    def onGetPointsData(self, points):
        JS_CODE = None
        print('getData:', len(points), points)
        self.view.page().runJavaScript(JS_CODE.removeOverlay)
        points = ['new BMap.Point({},{})'.format(gps.longitude, gps.latitude) for gps in points]
        pointsStr = ',\n\t'.join(points)
        jsStr = JS_CODE.addOverlay.replace('ckzlt_points', pointsStr)
        self.view.page().runJavaScript(jsStr)
        
    def createScroll(self):
        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(200, 100)
        grid = QGridLayout()
        self.topFiller.setLayout(grid)
        for i in range(2):
            bt = QPushButton('123', self)
            grid.addWidget(bt, i, 0)
        scroll = QScrollArea()
        scroll.setWidget(self.topFiller)
        scroll.setGeometry(0, 0, 50, 50)
        scroll.setMinimumSize(50, 50)
        # scroll.resize(1, 1)
        self.devGrid = grid
        self.scroll = scroll
        return scroll
    
    def subScribe(self, *args):
        print(args)
        
    def register(self, *args):
        print(args)

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        self.initBrowser()
        grid.addWidget(self.createButton('Subscribe', self.subScribe), 1, 1)
        grid.addWidget(self.createButton('Register', self.register), 1, 3)
        grid.addWidget(self.view, 3, 0, 3, 4)
        self.setLayout(grid)
        # self.setGeometry(0, 0, 1024, 768)
        self.setGeometry(0, 0, 1024, 768)
        # self.showMinimized()
        self.setWindowTitle('BuriedLove')
        self.show()


def browserGo():
    app = QApplication(sys.argv)
    yield Browser()
    sys.exit(app.exec_())


if __name__ == '__main__':
    bg = browserGo()
    ex = next(bg)
    next(bg)
