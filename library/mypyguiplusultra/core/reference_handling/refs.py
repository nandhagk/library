import weakref

class Ref:
    def __init__(self, item, refType = weakref.ref):
        self.refType = refType
        self.ref = self.refType(item) if item is not None else None

    def set(self, item):
        self.ref = self.refType(item) if item is not None else None

    def __call__(self):
        return self.ref() if self.ref is not None else None

def createRef(item = None):
    if hasattr(item, '__func__'):
        return Ref(item, weakref.WeakMethod)
    return Ref(item)
