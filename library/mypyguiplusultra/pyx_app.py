from mypyguiplusultra.pyx.stdlib import Body
from mypyguiplusultra.services import WindowProvider
from mypyguiplusultra.objects.dom_linker import linkDom

from threading import Thread

class PYXApp:
    def __init__(self, globalStyleSheet, minimumWindowSize):
        self.globalStyleSheet = globalStyleSheet
        self.windowProvider = WindowProvider()
        self.windowProvider.setMinimumWindowSize(minimumWindowSize)
        '''Deals with the pyqt side of things :)'''

        Thread(target=self.windowProvider.run).start() # Just run the windowProvider in another thread
        # *For rest of the services we will use the QThreadPool to get work done :)

    def render(self, body):
        assert isinstance(body, Body), "body given to the application for rendering must be an instance of mypyguiplusultra.pyx.stdlib.Body"
        print()
        root = body.body() # Gets the body of the application

        linkDom(root, self.globalStyleSheet, self.windowProvider) # Adds render nodes to the dom nodes
        root.renderNode.setHeirarchy() # Moves the render nodes around based on their styles
        root.renderNode.layout() # Positions each element
        root.renderNode.renderWorker.paint() # Paints everything (creates QtNodes here)

        # self.windowProvider.setTitle(self.initialTitle)
        self.windowProvider.on.end.wait()
        root.remove(_relayout=False, _removeFromParentList=False)
