
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from .render_worker import RenderWorker
from .qelem_helper import QElemHelper
from PyQt6 import QtNetwork
from PyQt6.QtCore import QSize, QUrl, Qt

class ImageRenderWorker(RenderWorker):
    def __init__(self):
        super().__init__()
        self.paintedNode = False
        self.pixmap = QPixmap()

    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot update it
            print('Node is no longer alive boss')
            return

        with QElemHelper.use(self.mainQ, node.renderInformation) as helper:
            helper.setPosition(node.master().renderInformation.scroll_offset_x, node.master().renderInformation.scroll_offset_y)
            helper.setOpacity()
            helper.setZIndex()
            helper.setFlags()

            size = QSize(int(node.renderInformation.width), int(node.renderInformation.height))
            if self.mainQ.pixmap().size() != size:
                self.mainQ.setPixmap(self.pixmap.scaled(size, transformMode=Qt.TransformationMode.SmoothTransformation))
                # print("need to rmap")

    def handleResponse(self, response):
        print("response is came")
        if self.node() is None or self.node().domNode() is None:return
        if response.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            self.pixmap.loadFromData(response.readAll())
            self.mainQ.setPixmap(self.pixmap)
            if self.paintedNode:self._update()
        else:
            print(response.error())
            print("ERROR IN LOADING RESOURCE")

        # TODO: If there are any memoery leaks, consider these two lines :)
        self.nam.disconnect()
        self.nam.deleteLater()


    def loadImageFromSource(self, src):
        # TODO: Fix the lag prodyced frmo getting over here
        req = QtNetwork.QNetworkRequest(QUrl(src))
        print("requesting resource")
        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)


    def _paint(self, qparent = None):
        self.paintedNode = True
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()
        self.mainQ = QGraphicsPixmapItem(self.pixmap, qparent)
        if node.domNode().attrs.get("clickable"):
            self.setClickable(True)
        self._connectEvents() # Connect events to the eventListener

        self._update(updateSlaves=False) # Basically just draws it :)
