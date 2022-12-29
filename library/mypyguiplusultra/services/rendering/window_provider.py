from mypyguiplusultra.core.events import EventEmitter, Event
from .myqt import Window, App, AlertWindow, ConfirmWindow

class WindowProvider:
    def __init__(self):
        self.on = EventEmitter()
        self.on.ready = Event('ready', oneTimeOnly=True)
        self.on.end = Event('ready', oneTimeOnly=True)
        self.minimumWindowSize = (None, None)

    def setTitle(self, title):
        self.window.setWindowTitle(title)

    def _setMinimumWindowSize(self):
        if self.minimumWindowSize[0] is not None:
            self.window.setMinimumWidth(self.minimumWindowSize[0])
        if self.minimumWindowSize[1] is not None:
            self.window.setMinimumHeight(self.minimumWindowSize[1])

    def setMinimumWindowSize(self, size):
        self.minimumWindowSize = size
        if getattr(self, 'window', None) is not None:
            self._setMinimumWindowSize()

    def inform(self, message, title="Information"):
        '''Shows a dialog box with some text'''
        return AlertWindow(self.window, message, title).wait()

    def confirm(self, question, title="Confirmation"):
        '''Shows a dialog box to confirm some action'''
        return ConfirmWindow(self.window, question, title).wait()



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
