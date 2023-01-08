from types import SimpleNamespace

class Object(SimpleNamespace):
    def __getattr__(self, name):
        return None

    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def copy(self):
        return Object(**self.__dict__)

    def items(self):
        return self.__dict__.items()

    def __getitem__(self, name):
        return self.get(name)