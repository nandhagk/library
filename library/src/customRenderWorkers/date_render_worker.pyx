
from PyQt6.QtWidgets import QGraphicsProxyWidget, QDateEdit , QStyle
from mypyguiplusultra.tools.renderWorkers.render_worker import RenderWorker
from mypyguiplusultra.tools.renderWorkers.qelem_helper import QElemHelper
from PyQt6.QtCore import Qt
from mypyguiplusultra.objects.render_tree.layout_helper import LayoutHelper


class DateRenderWorker(RenderWorker):
    def remove(self):

        self.calendarEditWidget.deleteLater()
        del self.calendarEditWidget
        super().remove()

    def layout(self, *args, **kwargs):
        return LayoutHelper.layoutTextNode(self.node(), *args, **kwargs)

    def _update(self, updateSlaves=True):
        node = self.node()
        if node is None: # If reference to the node does not exist, we cannot update it
            print('Node is no longer alive boss')
            return
        self.calendarEditWidget.setFixedWidth(int(node.renderInformation.width))
        self.calendarEditWidget.setFixedHeight(int(node.renderInformation.height))
        #  if self.calendarEditWidget.text() else node.renderInformation.placeholder_color
        # print(node.renderInformation.placeholder_color)
        # print(node.renderInformation.foreground_color, self.calendarEditWidget.text(), 1)
        self.calendarEditWidget.setStyleSheet(f"""QDateEdit {'{'}
            background-color:{node.renderInformation.background_color};
            color:{node.renderInformation.foreground_color};
            border-radius:{node.renderInformation.border_top_left_radius}px {node.renderInformation.border_top_right_radius}px;
            border:none;
            border-bottom-style:solid;
            border-color:{node.renderInformation.border_color};
            border-bottom-width:{node.renderInformation.border_width};
        {'}'}
        """)
        # TODO: Remove bacground color of QGraphicsPRoxyItem
        self.calendarEditWidget.setFont(node.renderInformation.font)
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

    def updateTextContent(self, t):
        self.node().domNode().content = t

    def setText(self, t):
        self.calendarEditWidget.setText(t)

    def _paint(self, qparent = None):
        node = self.node() # The renderNode
        if node is None: # If reference to the node does not exist, we cannot paint it
            print('Node is no longer alive boss')
            return

        qparent = self._getParent()

        self.mainQ = QGraphicsProxyWidget(qparent) # Create the QGraphicsItem
        self.calendarEditWidget = QDateEdit ()
        # self.calendarEditWidget.setPlaceholderText(self.node().domNode().attrs.get('placeholder', ''))
        self.mainQ.setWidget(self.calendarEditWidget)

        self._connectEvents() # Connect events to the eventListener
        # self.calendarEditWidget.textChanged.connect(self.updateTextContent)

        self._update(updateSlaves=False) # Basically just draws it :)
