from mypyguiplusultra.core.events import EventEmitter, Event
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView
from PyQt6.QtCore import pyqtSlot

from PyQt6.QtNetwork import QNetworkAccessManager

class App(QApplication):
    @pyqtSlot(tuple)
    def invokeFunction(self, tup):
        tup[0](*tup[1], **tup[2])

class Window(QMainWindow):

    def __init__(self):
        self.on = EventEmitter()
        self.nam = QNetworkAccessManager()
        self.on.resize = Event('resize')
        super().__init__()

    def resizeEvent(self, event):
        self.on.resize.resolve(event)
        super().resizeEvent(event)


class WindowProvider:
    def __init__(self):
        self.on = EventEmitter()
        self.on.ready = Event('ready', oneTimeOnly=True)
        self.on.end = Event('ready', oneTimeOnly=True)
        self.minimumWindowSize = (None, None)


    def _setMinimumWindowSize(self):
        if self.minimumWindowSize[0] is not None:
            self.window.setMinimumWidth(self.minimumWindowSize[0])
        if self.minimumWindowSize[1] is not None:
            self.window.setMinimumHeight(self.minimumWindowSize[1])

    def setMinimumWindowSize(self, size):
        self.minimumWindowSize = size
        if getattr(self, 'window', None) is not None:
            self._setMinimumWindowSize()



    def run(self):
        '''Runs the mainloop'''
        self.root = App([])
        '''pyqt app'''
        self.window = Window() # The main window
        self.window.show()
        self._setMinimumWindowSize()
        self.root.aboutToQuit.connect(lambda:self.on.end.resolve(True)) # When the gui closes we have to resolve it

        self.on.ready.resolve(True) # The gui is now ready
        self.root.exec()
