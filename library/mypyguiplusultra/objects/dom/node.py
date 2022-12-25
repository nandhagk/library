from __future__ import annotations
from mypyguiplusultra.core import createRef
from .style_container import StyleContainer
from .state_maintainers import ClassList, StateContainer
from mypyguiplusultra.core.events import EventEmitter, Event

def propogateEvent(e):
    e[0].ignore()


class DOMNode:
    '''
    The building block of the dom
    NOTE: Remember that the renderNode is created in the layouting step and so any element created after that must have its render node added
    NOTE: Remember that styles are computed and set after creation of the cssom, so any element created after this must have its styles calculated
    '''
    __ignore__ = {'parent'}
    def __init__(
        self,
        tag      : str            = 'div',
        attrs    : Object         = {},
        children : list[DOMNode | Component | ""]  = [],
    ):
        # Descriptors
        self.tag        = tag
        '''The tag name of the element'''
        self.id         = attrs.get('id')
        '''The id of this element (as specified in the html)'''
        self.classList = ClassList(createRef(self), attrs.get('class', "").split())
        '''A collection of classes associated with the element'''
        self.state      = StateContainer(createRef(self), attrs.get('state', ('',))) # `''` implies default state
        '''The current state of the element'''

        # View
        self.styles    = StyleContainer(self)
        '''The styles associated with the element'''
        self.renderNode : RenderNode = None
        '''The object tasked with rendering me on the screen'''

        # Misc
        self.attrs     = attrs.copy()
        '''An object that contains all properties defined in the html'''
        self.content = ''
        '''
        The textual content in the element
        '''


        # In Events we can set ignore() to propogate the event to parent (dont propoaget hover start and hover end)
        # https://doc.qt.io/qt-6/qgraphicsitem.html#protected-functions
        # TODO: Link all of these events (qelem_handler._connectEvents)
        self.on = EventEmitter()

        self.on.key = Event('key')

        self.on.click = Event('click')
        self.on.click.subscribe(propogateEvent)

        self.on.focus = Event('focus') # NOTE: For an element to be focusable, it must be declared in the qitem
        self.on.unfocus = Event('unfocus') # textRenderWorker does this by default
        self.on.focuswithin = Event('focuswithin')
        self.on.unfocuswithin = Event('unfocuswithin')

        self.on.focus.subscribe(lambda e:self.state.add('focus'), weakify=False)
        self.on.unfocus.subscribe(lambda e:self.state.remove('focus'), weakify=False)

        self.on.focus.subscribe(self.on.focuswithin.resolve)
        self.on.unfocus.subscribe(self.on.unfocuswithin.resolve)

        self.on.focuswithin.subscribe(lambda e:self.state.add('focus-within'), weakify=False)
        self.on.unfocuswithin.subscribe(lambda e:self.state.remove('focus-within'), weakify=False)
        self.on.focuswithin.subscribe(lambda e:self.parent().on.focuswithin.resolve(e) if self.parent() is not None else 0, weakify=False)
        self.on.unfocuswithin.subscribe(lambda e:self.parent().on.unfocuswithin.resolve(e) if self.parent() is not None else 0, weakify=False)

        self.on.hoverStart = Event('hoverStart')
        self.on.hoverEnd = Event('hoverEnd')

        self.on.hoverStart.subscribe(lambda e:self.state.add('hover'), weakify=False)
        self.on.hoverEnd.subscribe(lambda e:self.state.remove('hover'), weakify=False)

        self.on.scroll = Event('scroll')
        self.on.scroll.subscribe(self.handleScroll)

        # Heirarchy
        self.parent    = createRef()
        '''The heirarchichal parent of this element'''
        self.children  = []
        '''List of elements which are children of me'''
        self.componentChildren = []
        '''List of components who are a child of me'''

        for item in children:
            if isinstance(item, str):
                self.content += item # If it was a string just add it to our content
                continue
            self.appendChild(item, _link=False) # If it is another domnode or a component just append it

    def remove(self, _relayout=True, _removeFromParentList=True):
        for component in self.componentChildren:
            component.unmount(_notifyNode=False)
        self.componentChildren.clear()

        for child in self.children:
            child.remove(_relayout=False, _removeFromParentList=False)
        self.children.clear()
        self.renderNode.remove()

        if _removeFromParentList:
            self.parent().children.remove(self)

        if _relayout:
            currNode = self.renderNode
            while currNode != currNode.master():
                currNode = currNode.master()
            currNode.layout()
            currNode.renderWorker.update()
        del self.renderNode

    def handleScroll(self, e):
        e[0].setAccepted(self.renderNode.handleScroll(e[0].delta(), e[0].modifiers()))


    def appendChild(self, child, _link = True, _relayout=True, _parent_components = ()):
        if not isinstance(child, DOMNode):# If the child is a component
            self.componentChildren.append(child) # *As we need to maintain reference of the component
            child.parentNode.set(self) # Provide reference to the component's parent
            xs = child.body() # Get the body of the component and mount it
            if xs is None:
                print("ERROR:",child, "body is not returning an element")
                return
            _parent_components = _parent_components + (child,)
            self.appendChild(xs, _link=_link, _relayout=_relayout, _parent_components = _parent_components) # Append the
            return

        # If the child is a dom node
        self.children.append(child) # Append it as a child
        child.parent.set(self) # Provide reference to its parent

        from ..cssom import StyleSheet

        if _parent_components:
            child.styles.scopedStyleSheet = StyleSheet()
        for i in _parent_components: # Set the body nodes of the components if any (also set scoped stylesheets)
            # NOTE: For now scoped stylesheets are not merged (lowest level component is taken)
            # i = _parent_components.pop(0)
            i.bodyNode.set(child) # Provide reference of the node to the component
            i.onMount()

            if i.scopedStyleSheet is None:continue
            child.styles.scopedStyleSheet.merge(i.scopedStyleSheet)

        if _link:
            # TODO: ALl this is little janky, edit this only if some problems are caused lmao
            from ..dom_linker import linkNode, traverseTree
            gss = self.styles.globalStyleSheet
            wp = self.renderNode.windowProvider()
            linkNode(child, self, gss, wp)
            traverseTree(child, linkNode, gss, wp)

            currNode = self.renderNode
            while currNode != currNode.master():
                currNode = currNode.master()

            from mypyguiplusultra.objects.cssom.css_enums import Position
            if self.styles.position == Position.absolute or self.styles.position == Position.relative:
                closestRelative = self.renderNode
            else:
                closestRelative = self.renderNode.closestRelative()
            child.renderNode.setHeirarchy(closestRelative, currNode)

            if _relayout:
                currNode.layout()
                child.renderNode.renderWorker.paint()
                currNode.renderWorker.update()

    def _onStateChange(self, added=None, removed=None, updateStyles=True):
        # In the future if stateChange event is needed, here you go
        if updateStyles:
            self.styles.computeStyles()

    def _onClassChange(self, added=None, removed=None, updateStyles=True):
        # NOTE: If in the future classChange event is needed, here you go
        if updateStyles:
            self.styles.computeStyles()

    def _onStyleChange(self):
        self.renderNode.reflow().renderWorker.update()


    def __eq__(self, other):
        return other is self

    def __repr__(self):
        attrs = ' '.join(f'{key}="{value}"' for key, value in self.attrs.items())
        attrs = (' ' + attrs) if attrs else ''
        return f'<{self.tag}{attrs}>{f"...({len(self.children)})..." if self.children else ""}</{self.tag}>'
