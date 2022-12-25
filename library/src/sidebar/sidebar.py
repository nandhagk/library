# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('./sidebar.css'))

from mypyguiplusultra.core import createRef

from .navItem import NavItem
from ..pages import Destinations

from PyQt6.QtWidgets import QGraphicsItem

@styles
class Sidebar(pyx.Component):
    def init(self):
        self.activeItem = createRef()

    def navigate(self, item):
        if item.props['destination'] == self.props['currentPage']():return
        self.props['currentPage'].set(item.props['destination'])
        self.activeItem().bodyNode().state.remove('active')
        self.activeItem().bodyNode().renderNode.renderWorker.setClickable(True)
        self.activeItem.set(item)
        self.activeItem().bodyNode().state.add('active')
        self.activeItem().bodyNode().renderNode.renderWorker.setClickable(False)


    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container', 'qflags': (QGraphicsItem.GraphicsItemFlag.ItemIsFocusable,)}, "", pyx.pyx_factory.createElement(NavItem, {'destination': Destinations.search, 'callback': self.navigate, 'active': True, 'ref': self.activeItem}), "", pyx.pyx_factory.createElement(NavItem, {'destination': Destinations.browse, 'callback': self.navigate}), "", pyx.pyx_factory.createElement(NavItem, {'destination': Destinations.add, 'callback': self.navigate}), "", )
