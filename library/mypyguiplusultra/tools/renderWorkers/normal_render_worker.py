
from PyQt6.QtWidgets import QGraphicsPathItem
from .render_worker import RenderWorker
from .qelem_helper import QElemHelper
from PyQt6.QtCore import Qt

# TODO LIST:
#     - Now just get started on the project

#     - Z index handling can be done in the future only if needed (worst case we can explitly set z index)
#     - (we can even have something rudimentary like zindex = master.zindex + relative z index)

#     - Text rendering

#     - Flags like scroll and maskChildElements

class NormalRenderWorker(RenderWorker):
    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot update it
            print('Node is no longer alive boss')
            return

        with QElemHelper.use(self.mainQ, node.renderInformation) as helper:
            helper.setPath()

            helper.setPosition(node.master().renderInformation.scroll_offset_x, node.master().renderInformation.scroll_offset_y)
            helper.setOpacity()
            helper.setZIndex()

            helper.setFlags()

            helper.setBorder()

            helper.setBrush()

        if updateSlaves:
            self._updateSlaves()

    def _paint(self, qparent = None):
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()
        self.mainQ = QGraphicsPathItem(qparent) # Create the QGraphicsItem

        self._connectEvents() # Connect events to the eventListener
        if node.domNode().attrs.get("clickable"):
            self.setClickable(True)
        self._update(updateSlaves=False) # Basically just draws it :)

        self._paintSlaves() # Paint our slaves

    def handleScroll(self, delta, modifiers):
        delta /= 5
        node = self.node()
        ri = node.renderInformation
        if not (ri.allow_scroll[0] or ri.allow_scroll[1]):return False # This element does not have scrolling enabled
        if all(ri.allow_scroll): # If the element expects scrolling in both directions,
            yDir = Qt.KeyboardModifier.ShiftModifier not in modifiers
        else:yDir = ri.allow_scroll[1] # Otherwise the direction of scroll is whatever it allows

        if yDir: # Scrolling done in y direction
            node.updateScrollOffset(dy=delta)
        else: # Scrolling done in x direction
            node.updateScrollOffset(dx=delta)
        node.renderWorker.update()


        return True
