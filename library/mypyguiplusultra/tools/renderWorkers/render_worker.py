from mypyguiplusultra.objects.render_tree.layout_helper import LayoutHelper
from PyQt6.QtCore import QMetaObject, Q_ARG, Qt
from mypyguiplusultra.core import createRef
from PyQt6.QtGui import QCursor
class RenderWorker:
    def __init__(self):
        self.node = createRef()
        self.mainQ = None

    def notifyNodeOfPaint(self):
        self.node().domNode()._notifyPaint()

    def layout(self, *args, **kwargs):
        return LayoutHelper.layoutBoxNode(self.node(), *args, **kwargs)

    def reflow(self, *args, **kwargs):
        return LayoutHelper.reflow(self.node(), *args, **kwargs)

    def _getParent(self):
        return self.node().master().renderWorker.mainQ

    def _paint(self):
        '''
        Overload this function
        Params:
            qparent: QGraphicsItem (the qt object that is the master of this slave)
        '''

    def _paintSlaves(self):
        '''Calls _paint on each slave'''
        node = self.node()
        for i in node.slaves:
            for slave in node.slaves[i]:
                slave().renderWorker._paint()

    def _update(self, updateSlaves=True):
        '''
        Overload this function
        Params:
            updateSlaves: Set to true when the slaves also have to be updated (only set to false on initial paint i think)
        '''

    def _updateSlaves(self, updateSlaves=True):
        '''Calls _paint on each slave'''
        node = self.node()
        for i in node.slaves:
            for slave in node.slaves[i]:
                slave().renderWorker._update(updateSlaves=updateSlaves)

    def _connectEvents(self):
        '''Connects events on the qgraphics item to the event listener :)'''
        self.mainQ.setAcceptHoverEvents(True)

        if self.node().domNode().attrs.get('qflags') is not None:
            self.mainQ.setFlags(*self.node().domNode().attrs.get('qflags'))
            
        # NOTE: If errors in this are like not fine, consider having references return like a `RecursiveNone` instead of normal None
        self.mainQ.mousePressEvent = lambda e:(self.mainQ.__class__.mousePressEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.click.resolve((e, self.node().domNode()))
        self.mainQ.hoverEnterEvent = lambda e:(self.mainQ.__class__.hoverEnterEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.hoverStart.resolve((e, self.node().domNode()))
        self.mainQ.hoverLeaveEvent = lambda e:(self.mainQ.__class__.hoverLeaveEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.hoverEnd.resolve((e, self.node().domNode()))
        self.mainQ.focusInEvent = lambda e:(self.mainQ.__class__.focusInEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.focus.resolve((e, self.node().domNode()))
        self.mainQ.focusOutEvent = lambda e:(self.mainQ.__class__.focusOutEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.unfocus.resolve((e, self.node().domNode()))
        self.mainQ.wheelEvent = lambda e:(self.mainQ.__class__.wheelEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.scroll.resolve((e, self.node().domNode()))
        self.mainQ.keyPressEvent = lambda e:(self.mainQ.__class__.keyPressEvent(self.mainQ, e) if getattr(self, 'mainQ', None) is not None else 0) is None and self.node().domNode().on.key.resolve((e, self.node().domNode()))


    def handleScroll(self, delta, modifiers):
        return False
    def setClickable(self, enabled):
        if enabled:
            self.mainQ.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.mainQ.setCursor(QCursor())

    def remove(self):
        # self.mainQ.setParentItem(None)
        self.mainQ.scene().removeItem(self.mainQ)
        del self.mainQ

    def paint(self, *args, **kwargs):
        '''Invoeks the _paint function in the thread the gui is present in'''
        self.__invokeMethod(self._paint, *args, **kwargs)

    def update(self, *args, **kwargs):
        '''Invokes the _update function in the gui thread'''
        self.__invokeMethod(self._update, *args, **kwargs)

    def __invokeMethod(self, method, *args, **kwargs):
        '''Invokes the method in the main render loop'''
        QMetaObject.invokeMethod(
            self.node().windowProvider().root,
            'invokeFunction',
            Q_ARG(
                tuple, (
                    method,
                    args, kwargs
                )
            )
        )
