
from PyQt6.QtWidgets import QGraphicsTextItem, QStyle, QGraphicsPathItem
from PyQt6.QtGui import QFont, QCursor, QTextCursor
from PyQt6.QtCore import Qt
from .render_worker import RenderWorker
from .qelem_helper import QElemHelper
from mypyguiplusultra.objects.render_tree.layout_helper import LayoutHelper


class TextItem(QGraphicsTextItem):
    def paint(self, *args): # Apparently overriding in python is like mad slow so lets not do that :)
        args[1].state = args[1].state & ~QStyle.StateFlag.State_HasFocus # Basically remove that annoying dashed border on focus gain
        super().paint(*args)

class TextRenderWorker(RenderWorker):
    def layout(self, *args, **kwargs):
        return LayoutHelper.layoutTextNode(self.node(), *args, **kwargs)

    # def remove(self):
    #     self.textQ.scene().removeItem(self.textQ)
    #     del self.textQ
    #     super().remove()

    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot update it
            print('Node is no longer alive boss')
            return

        # self.textQ.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.textQ.setPlainText(node.domNode().content)
        # self.textQ.setHtml(f'<{node.renderInformation.text_align}>{node.domNode().content}</{node.renderInformation.text_align}>')
        self.textQ.setDefaultTextColor(QElemHelper._getForegroundColor(node.renderInformation))
        self.textQ.setTextWidth(node.renderInformation.width - node.renderInformation.text_x_offset)
        self.textQ.setFont(node.renderInformation.font)
        self.textQ.setPos(node.renderInformation.text_x_offset, node.renderInformation.text_y_offset)

        with QElemHelper.use(self.mainQ, node.renderInformation) as helper:
            helper.setPath()

            helper.setPosition(node.master().renderInformation.scroll_offset_x, node.master().renderInformation.scroll_offset_y)
            helper.setOpacity()
            helper.setZIndex()

            helper.setFlags()

            helper.setBorder()

            helper.setBrush()


    def _paint(self, qparent = None):
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()
        self.mainQ = QGraphicsPathItem(qparent)
        self.textQ = QGraphicsTextItem(self.mainQ) # Create the QGraphicsItem
        self.textQ.document().setDocumentMargin(0)

        self._connectEvents() # Connect events to the eventListener
        if self.node().domNode().attrs.get('qtextflags') is not None:
            self.textQ.setTextInteractionFlags(*self.node().domNode().attrs.get('qtextflags'))
        if node.domNode().attrs.get("clickable"):
            self.setClickable(True)
        self._update(updateSlaves=False) # Basically just draws it :)
        self.notifyNodeOfPaint()
