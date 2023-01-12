from mypyguiplusultra.core import createRef
from .information_containers import LayoutInformationContainer, RenderInformationContainer
from mypyguiplusultra.objects.cssom import css_enums
from .layout_helper import LayoutHelper

class RenderNode:
    '''
    BOX MODEL:
        -> width and height define the end size (everything except for margins)
        -> padding and margin dont overlap
        -> margins overlap
    '''
    def __init__(
        self,
        domNode,
        windowProvider,
        renderWorker
    ):

        self.domNode = createRef(domNode)
        '''The domnode this rendernode is representing'''

        self.closestRelative = createRef()
        '''Closest relative of the element'''

        # Information containers
        self.layoutInformation = LayoutInformationContainer()
        '''
        Stores information about the layout of the element
        NOTE: The values are in absolute values (px)
        '''
        self.renderInformation = RenderInformationContainer()
        '''
        Stores information on how the element is to be rendered
        NOTE: The values are in absolute values (px)
        '''

        # Heirarchy
        self.master = createRef()
        '''
        The element with respect to which the origin is set
        NOTE: Units like %, em etc. are also calculated wrt to this element
        '''
        self.slaves : dict[int, list[RenderNode]] = {}
        '''
        All elements this element is the master to
        Stored in a dictionary that maps zIndex to lists of renderNodes (stored in the order they are to be rendered)
        NOTE: Removal and addition of foreign slaves must be done by their parents and will not be done by their master
        '''
        self.windowProvider = createRef(windowProvider)
        '''Reference to the windowProvider'''

        from mypyguiplusultra.core.util import Object
        self.qNamespace = Object()

        self.renderWorker = renderWorker
        '''The q :)'''
        self.renderWorker.node.set(self)

    def setRenderInformation(self, hidden=False):
        dn = self.domNode()

        self.layoutInformation.calculated_content_size = None # This property is set on reflows
        if hidden:
            self.renderInformation.init()
            return
        self.renderInformation.x = self.layoutInformation.x
        self.renderInformation.y = self.layoutInformation.y
        self.renderInformation.width = self.layoutInformation.width
        self.renderInformation.height = self.layoutInformation.height
        self.renderInformation.content_width = self.layoutInformation.content_width
        self.renderInformation.content_height = self.layoutInformation.content_height
        self.renderInformation.scroll_region_x = self.layoutInformation.scroll_region_x
        self.renderInformation.scroll_region_y = self.layoutInformation.scroll_region_y

        self.renderInformation.mask_children = dn.styles.overflow_x in [css_enums.Overflow.hidden, css_enums.Overflow.scroll] or dn.styles.overflow_y in [css_enums.Overflow.hidden, css_enums.Overflow.scroll]
        self.renderInformation.allow_scroll = (dn.styles.overflow_x == css_enums.Overflow.scroll, dn.styles.overflow_y == css_enums.Overflow.scroll)

        self.renderInformation.opacity = dn.styles.opacity
        self.renderInformation.z_index = dn.styles.z_index

        # self.renderInformation.border_bottom_left_radius = self.getValue(dn.styles.border_bottom_left_radius)
        # self.renderInformation.border_bottom_right_radius = self.getValue(dn.styles.border_bottom_right_radius)
        self.renderInformation.border_top_left_radius = self.getValue(dn.styles.border_top_left_radius)
        self.renderInformation.border_top_right_radius = self.getValue(dn.styles.border_top_right_radius)

        self.renderInformation.border_style = dn.styles.border_style

        self.renderInformation.background_color = dn.styles.background_color if dn.styles.background_color is not None else 'transparent'
        self.renderInformation.foreground_color = dn.styles.color if dn.styles.color is not None else 'transparent'
        self.renderInformation.placeholder_color = dn.styles.placeholder_color if dn.styles.placeholder_color is not None else 'transparent'

        self.renderInformation.border_color = dn.styles.border_color if dn.styles.border_color is not None else ''
        self.renderInformation.border_width = self.getValue(dn.styles.border_width)
        self.renderInformation.border_style = dn.styles.border_style
        self.updateScrollOffset()

    def _getMultiplier(self, unit):
        if unit == css_enums.Unit.px:return 1
        elif unit == css_enums.Unit.null:return 0

        # God knows how these even work lmao
        elif unit == css_enums.Unit.em:return 16
        elif unit == css_enums.Unit.rem:return 16

        # Viewport
        elif unit == css_enums.Unit.viewport_height:return self.windowProvider().window.size().height() / 100
        elif unit == css_enums.Unit.viewport_width:return self.windowProvider().window.size().width() / 100

        # Percentage
        elif unit == css_enums.Unit.master_height:return self.master().layoutInformation.height / 100
        elif unit == css_enums.Unit.master_width:return self.master().layoutInformation.width / 100
        elif unit == css_enums.Unit.self_height:return self.renderInformation.height / 100
        elif unit == css_enums.Unit.self_width:return self.layoutInformation.width / 100

    def getValue(self, cssValue, default=0):
        try:
            return self._getMultiplier(cssValue[1]) * cssValue[0]
        except:
            return default

    def layout(self, *args, **kwargs):
        return self.renderWorker.layout(*args, **kwargs)

    def reflow(self):
        return self.renderWorker.reflow()

    def addSlave(self, slave, z_index):
        '''Registers a slave'''
        if self.slaves.get(z_index) is None:
            self.slaves[z_index] = list()
        self.slaves[z_index].append(createRef(slave))
        slave.master.set(self)

    def remove(self):
        self.master().removeSlave(self, self.domNode().styles.z_index)
        self.renderWorker.remove()
        del self.renderWorker

    def removeSlave(self, slave, z_index):
        '''Removes a registered slave on the element'''
        try:
            for i in range(len(self.slaves[z_index])):
                if self.slaves[z_index][i]() is slave:
                    self.slaves[z_index].pop(i)
                    break
            # self.slaves[z_index].remove(slave)
        except:pass

    def updateScrollOffset(self, dx = 0, dy = 0):

        self.renderInformation.scroll_offset_x += dx
        self.renderInformation.scroll_offset_y += dy

        self.renderInformation.scroll_offset_x = -min(max(self.renderInformation.scroll_region_x - self.renderInformation.content_width, 0), max(-self.renderInformation.scroll_offset_x,0))
        self.renderInformation.scroll_offset_y = -min(max(self.renderInformation.scroll_region_y - self.renderInformation.content_height, 0), max(-self.renderInformation.scroll_offset_y,0))


    def handleScroll(self, delta, modifiers):
        return self.renderWorker.handleScroll(delta, modifiers)

    def setHeirarchy(self, closestRelative, root):
        '''Sets the heirarchy of all elems'''
        self.closestRelative.set(closestRelative)

        if self.domNode().styles.overflow_x is not None or self.domNode().styles.overflow_y is not None: # or self.domNode().styles.opacity != 1:
            self.needsComposite = True # NOTE: Now overflow hidden is implicitly enforced

        if self.domNode().styles.position == css_enums.Position.absolute:
            # Absolute elements are slaves to the closest element with `position: relative`
            self.closestRelative().addSlave(self, self.domNode().styles.z_index if self.domNode().styles.z_index is not None else 1)
            # self.master().set(self.closestRelative())
            closestRelative = self
        elif self.domNode().styles.position == css_enums.Position.fixed:
            # Fixed elements are slaves to the root
            root.addSlave(self, self.domNode().styles.z_index if self.domNode().styles.z_index is not None else 1)
            # self.master().set(root)
            closestRelative = root
        elif self.domNode().styles.position == css_enums.Position.relative:
            # Relative elements register themselves as the closest relative element for their children
            self.domNode().parent().renderNode.addSlave(self, self.domNode().styles.z_index if self.domNode().styles.z_index is not None else 1)
            # self.master().set(self.domNode().parent().renderNode)
            closestRelative = self
        elif self.domNode().styles.position == css_enums.Position.static:
            # Static elements follow the normal flow of the document
            self.domNode().parent().renderNode.addSlave(self, self.domNode().styles.z_index if self.domNode().styles.z_index is not None else 1)
            # self.master().set(self.domNode().parent().renderNode)
        else:
            raise Exception('Invalid postition')
        for child in self.domNode().children:
            child.renderNode.setHeirarchy(closestRelative, root)
