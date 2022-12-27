from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from mypyguiplusultra.core import createRef
from .render_worker import RenderWorker
from .qelem_helper import QElemHelper
from PyQt6.QtCore import Qt

class GraphicsView(QGraphicsView):
    def scrollContentsBy(self, x, y):
        # Disable scrolling in the view itself :)
        pass

class RootRenderWorker(RenderWorker):
    def getWindowSize(self):
        size = self.node().windowProvider().window.size()
        return size.width(), size.height()

    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return
        self.qgs.setSceneRect(0, 0, node.renderInformation.width, node.renderInformation.height) # Update the size of the QGraphicsScene
        self.mainQ.setRect(0, 0, node.renderInformation.width, node.renderInformation.height) # Update the size of the QGraphicsItem

        QElemHelper.setBorder(self.mainQ, node.renderInformation)
        QElemHelper.setBrush(self.mainQ, node.renderInformation)

        if updateSlaves:
            self._updateSlaves(node)

    def _onResize(self, e):
        self.node().layout()
        self._update()

    def _connectEvents(self):
        super()._connectEvents()
        self.node().windowProvider().window.on.resize.subscribe(self._onResize)

    def _paint(self):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        self.qgs = QGraphicsScene()
        self.mainQ = QGraphicsRectItem()
        self._connectEvents()

        self.qgs.addItem(self.mainQ)

        self._update(updateSlaves=False)

        window = node.windowProvider().window
        self.qgv = GraphicsView(self.qgs, window) # Create the actual graphics view
        self.qgv.setViewportMargins(-1, -1, -1, -1) # Fixes the wierd ass shit they do in `fitInView`
        self.qgv.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.qgv.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        window.setCentralWidget(self.qgv)

        self._paintSlaves()
        self.notifyNodeOfPaint()
