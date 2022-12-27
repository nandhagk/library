from mypyguiplusultra.objects import DOMNode
from mypyguiplusultra.pyx import Component
from mypyguiplusultra.core.util import Object

globalObject = Object()


def setGlobalObject(obj):
    global globalObject
    globalObject = obj


def createElement(elem, attrs, *children):
    global globalObject
    try:
        attrs = Object(**attrs)
    except:
        print(attrs)

    ref = attrs.ref
    if ref is not None:
        del attrs.ref

    if type(elem) == str: # String element
        element = DOMNode(elem, attrs, children)
    elif isinstance(elem, type) and issubclass(elem, Component): # Create component
        attrs.globalObject = globalObject
        element = elem(attrs, children)
    else: # The elem is a macro
        attrs.globalObject = globalObject
        element = elem(attrs, children)

    if ref is not None:ref.set(element)

    return element
