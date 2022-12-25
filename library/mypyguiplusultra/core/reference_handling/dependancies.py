class Dependancy:
    def __init__(self, value, consequence):
        self.value = value
        self.consequence = consequence

    def set(self, value):
        '''If a new object needs to become the value'''
        self.value = value
        self.onChange()

    def modify(self, modifier, *args, **kwargs):
        '''Call this when a function modifies the value (only useful if value is immutable)'''
        modifier(self.value, *args, **kwargs)
        self.onChange()

    def onChange(self):
        '''Calls the consequence when the value changes'''
        if self.consequence() is not None:
            self.consequence()()

    def __call__(self):
        return self.value


def createDependancy(value, consequence = None):
    from .refs import createRef
    return Dependancy(value, createRef() if consequence is None else consequence)
