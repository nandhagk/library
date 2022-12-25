from PyQt6.QtGui import QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt
from mypyguiplusultra.objects.cssom.css_enums import BorderStyle
from PyQt6.QtWidgets import QGraphicsItem

# TODO:
#   - Basically a lot of the time we are updating properties that dont really change
#       If we are getting performance issues, this is one place to look at
#       NOTE: Do not change it right now, only come back here if performance sucks ass

class HelperProxy:
    def __init__(self, qitem, renderInformation):
        self.mainQ = qitem
        self.renderInformation = renderInformation

    def __getattr__(self, name):
        return lambda *args, **kwargs:getattr(QElemHelper, name)(self.mainQ, self.renderInformation, *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(*exc_info):
        return

class QElemHelper:
    @staticmethod
    def setPath(qitem, renderInformation):
        path = QPainterPath()
        border = 2 * renderInformation.border_width
        path.addRoundedRect(0, 0, renderInformation.width - border, renderInformation.height - border, renderInformation.border_top_left_radius, renderInformation.border_top_right_radius)
        qitem.setPath(path)

    @staticmethod
    def setFlags(qitem, renderInformation):
        if renderInformation.mask_children:
            qitem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape, True)

    @staticmethod
    def setPosition(qitem, renderInformation, scrollOffsetX, scrollOffsetY):
        qitem.setPos(renderInformation.x + renderInformation.border_width + scrollOffsetX, renderInformation.y + renderInformation.border_width + scrollOffsetY)

    @staticmethod
    def setBorder(qitem, renderInformation):
        qitem.setPen(QElemHelper._getPen(renderInformation))

    @staticmethod
    def setOpacity(qitem, renderInformation):
        qitem.setOpacity(renderInformation.opacity)

    @staticmethod
    def setZIndex(qitem, renderInformation):
        qitem.setZValue(renderInformation.z_index)

    @staticmethod
    def setBrush(qitem, renderInformation):
        qitem.setBrush(QElemHelper._getBrush(renderInformation))

    @staticmethod
    def _getBrush(renderInformation):
        return QBrush(QElemHelper._getBackgroundColor(renderInformation))

    @staticmethod
    def _getBackgroundColor(renderInformation):
        return QColor(renderInformation.background_color)

    @staticmethod
    def _getForegroundColor(renderInformation):

        return QColor(renderInformation.foreground_color)

    @staticmethod
    def _getPen(renderInformation):
        pen = QPen(QColor(renderInformation.border_color), renderInformation.border_width)
        style = QElemHelper._getPenStyle(renderInformation)
        pen.setStyle(style)
        return pen

    @staticmethod
    def _getPenStyle(renderInformation):
        if renderInformation.border_width == 0 or renderInformation.border_style == BorderStyle.none:return Qt.PenStyle.NoPen

        if renderInformation.border_style == BorderStyle.solid:return Qt.PenStyle.SolidLine
        if renderInformation.border_style == BorderStyle.dashed:return Qt.PenStyle.DashLine
        if renderInformation.border_style == BorderStyle.dotted:return Qt.PenStyle.DotLine

        print("IDK wth this border style is") # debug
        return Qt.PenStyle.NoPen

    @staticmethod
    def use(qitem , renderInformation):
        return HelperProxy(qitem, renderInformation)
