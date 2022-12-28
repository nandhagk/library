import styles from "./sidebar.css"

from mypyguiplusultra.core import createRef

from .navItem import NavItem
from ..pages import Destinations

from PyQt6.QtWidgets import QGraphicsItem

@styles
class Sidebar(pyx.Component):
    def init(self):
        self.activeItem = createRef()


    def deactivate(self):
        if self.activeItem() is None:return
        self.activeItem().bodyNode().state.remove('active')
        self.activeItem().bodyNode().renderNode.renderWorker.setClickable(True)
        self.activeItem.set(None)

    def navigate(self, item):
        if item.props.destination == self.glob.currentPage():return
        self.glob.data = None
        self.glob.currentPage.set(item.props.destination)
        
        self.deactivate()
        self.activeItem.set(item)
        item.bodyNode().state.add('active')
        item.bodyNode().renderNode.renderWorker.setClickable(False)


    def body(self):
        return <div class="container" qflags={(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable,)}>
            <NavItem destination={Destinations.browse} callback={self.navigate} active={True} ref={self.activeItem}/>
            <NavItem destination={Destinations.search} callback={self.navigate}/>
            <NavItem destination={Destinations.add}    callback={self.navigate}/>
        </div>
