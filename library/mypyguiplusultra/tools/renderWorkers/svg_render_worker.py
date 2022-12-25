
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from .render_worker import RenderWorker
from .qelem_helper import QElemHelper

class SVGRenderWorker(RenderWorker):
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

            sx = node.renderInformation.width/self.mainQ.boundingRect().width()
            self.mainQ.setScale(sx) # NOTE: During layouting, it is required for height to be set using aspect-ratio


    def _paint(self, qparent = None):
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()
        self.mainQ = QGraphicsSvgItem(node.domNode().attrs['src'], qparent)
        if node.domNode().attrs.get("clickable"):
            self.setClickable(True)
        self._connectEvents() # Connect events to the eventListener

        self._update(updateSlaves=False) # Basically just draws it :)
