from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..dom_node import DOMNode

class MySet(dict):
    def __init__(self, *args):
        super().__init__((i, True) for i in args)

    def add(self, v):
        self[v] = True

    def remove(self, v):
        if v in self:del self[v]

    def contains(self, v):
        return v in self

    def issuperset(self, other):
        return set(self.values()).issuperset(other)

class ClassList(MySet):
    '''
    Stores the classes attributed to an element
    '''
    def __init__(self, element, args):
        super().__init__(*args)
        self.element = element

    def add(self, cls, updateStyles = True):
        if cls in self:return
        super().add(cls)
        self.element()._onClassChange(added = cls, updateStyles = updateStyles)

    def remove(self, cls, updateStyles = True):
        if cls in self:
            super().remove(cls)
        self.element()._onClassChange(removed = cls, updateStyles = updateStyles)

    def toggle(self, cls, updateStyles = True):
        if cls in self:
            self.remove(cls, updateStyles = updateStyles)
        else:
            self.add(cls, updateStyles = updateStyles)

    def __add__(self, cls):
        self.add(cls)

    def __sub__(self, cls):
        self.remove(cls)

class StateContainer(MySet):
    '''
    Stores the current state of the element
    '''
    def __init__(self, element, args):
        super().__init__(*args)
        self.element = element

    def add(self, state, updateStyles = True):
        if state in self:return
        super().add(state)
        self.element()._onStateChange(added = state, updateStyles = updateStyles)

    def toggle(self, state, updateStyles = True):
        if state in self:
            self.remove(state, updateStyles = updateStyles)
        else:
            self.add(state, updateStyles = updateStyles)

    def remove(self, state, updateStyles = True):
        if state in self:
            super().remove(state)
        self.element()._onStateChange(removed = state, updateStyles = updateStyles)

    def __add__(self, state):
        self.add(state)

    def __sub__(self, state):
        self.remove(state)
