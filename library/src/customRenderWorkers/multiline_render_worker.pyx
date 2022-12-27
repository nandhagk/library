
from PyQt6.QtWidgets import QGraphicsProxyWidget, QPlainTextEdit
from mypyguiplusultra.tools.renderWorkers.render_worker import RenderWorker
from mypyguiplusultra.tools.renderWorkers.qelem_helper import QElemHelper
from PyQt6.QtCore import Qt
from mypyguiplusultra.objects.render_tree.layout_helper import LayoutHelper


class MultiLineRenderWorker(RenderWorker):
    def remove(self):

        self.multLineEditWidget.deleteLater()
        del self.multLineEditWidget
        super().remove()

    def layout(self, *args, **kwargs):
        return LayoutHelper.layoutTextNode(self.node(), *args, **kwargs)
    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot update it
            print('Node is no longer alive boss')
            return
        self.multLineEditWidget.setFixedWidth(int(node.renderInformation.width))
        self.multLineEditWidget.setFixedHeight(int(node.renderInformation.height))
        #  if self.multLineEditWidget.text() else node.renderInformation.placeholder_color
        # print(node.renderInformation.placeholder_color)
        # print(node.renderInformation.foreground_color, self.multLineEditWidget.text(), 1)
        self.multLineEditWidget.setStyleSheet(f"""QPlainTextEdit {'{'}
            background-color:{node.renderInformation.background_color};
            color:{node.renderInformation.foreground_color};
            border-radius:{node.renderInformation.border_top_left_radius}px {node.renderInformation.border_top_right_radius}px;
            border:none;
            border-bottom-style:solid;
            border-color:{node.renderInformation.border_color};
            border-bottom-width:{node.renderInformation.border_width};
        {'}'}
        """)
        self.multLineEditWidget.setFont(node.renderInformation.font)
        with QElemHelper.use(self.mainQ, node.renderInformation) as helper:
            # helper.setPath()

            helper.setPosition(node.master().renderInformation.scroll_offset_x, node.master().renderInformation.scroll_offset_y)
            helper.setOpacity()

            helper.setZIndex()

            helper.setFlags()

            # helper.setBorder()

            # helper.setBrush()

        if updateSlaves:
            self._updateSlaves()

    def updateTextContent(self):
        self.node().domNode().content = self.multLineEditWidget.toPlainText()
        self.node().reflow().renderWorker.update()

    def setText(self, t):
        self.multLineEditWidget.setText(t)

    def _paint(self, qparent = None):
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()

        self.mainQ = QGraphicsProxyWidget(qparent) # Create the QGraphicsItem
        self.multLineEditWidget = QPlainTextEdit(self.node().domNode().content)
        # self.multLineEditWidget.setPlaceholderText(self.node().domNode().attrs.get('placeholder', ''))
        self.mainQ.setWidget(self.multLineEditWidget)
        self.multLineEditWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.multLineEditWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._connectEvents() # Connect events to the eventListener
        self.multLineEditWidget.textChanged.connect(self.updateTextContent)

        self._update(updateSlaves=False) # Basically just draws it :)
