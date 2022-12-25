from mypyguiplusultra.objects import DOMNode
from mypyguiplusultra.pyx import Component

def createElement(elem, attrs, *children):
    ref = attrs.get('ref')
    if ref is not None:
        del attrs['ref']

    if type(elem) == str: # String element
        element = DOMNode(elem, attrs, children)
    elif isinstance(elem, type) and issubclass(elem, Component): # Create component
        element = elem(attrs, children)
    else: # The elem is a macro
        element = elem(attrs, children)

    if ref is not None:ref.set(element)

    return element
