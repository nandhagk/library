from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSlot, Qt
from mypyguiplusultra.core.events import EventEmitter, Event


class App(QApplication):
    @pyqtSlot(tuple)
    def invokeFunction(self, tup):
        tup[0](*tup[1], **tup[2])

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.on = EventEmitter()
        # self.nam = QNetworkAccessManager() # This doesnt improve anything :(
        self.on.resize = Event('resize')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def resizeEvent(self, event):
        self.on.resize.resolve(event)
        super().resizeEvent(event)

class ConfirmWindow(QDialog):
    def __init__(self, window, question, title):
        super().__init__(window)
        self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(question)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    def wait(self):
        self.exec()
        return self.result()

class AlertWindow(QDialog):
    def __init__(self, window, message, title):
        super().__init__(window)
        self.setWindowTitle(title)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        alrt = QLabel(message)
        self.layout.addWidget(alrt)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def wait(self):
        self.exec()
        return True