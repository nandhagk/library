from mypyguiplusultra.core import createRef


class Component:
    scopedStyleSheet = None

    def __init__(self, props, slots):
        self.glob = props.globalObject
        del props.globalObject
        self.props = props

        self.slots = slots
        self.parentNode = createRef()
        self.bodyNode = createRef()
        self.init()

    def init(self):
        '''Override to do some extra tasks (like create references) during initialization'''

    def onMount(self):
        '''Called after the component has been mounted'''
        pass

    def onPaint(self):
        '''Called after painting has finished'''
        pass

    def onUnmount(self):
        '''Called after the component has been unmounted'''
        pass

    def body(self):
        '''Override to give the body of the component'''

    # def remount(self):
    #     '''Remounts the component onto a domnode'''

    def unmount(self, _notifyNode=True):
        '''Unmounts the component (NOTE: Setting _notifyNode to False will not do anything (it only calls Component.onUnmount))'''
        self.onUnmount()
        if _notifyNode:
            self.bodyNode().remove()
            self.parentNode().componentChildren.remove(self)

    def __eq__(self, other):
        return other is self
