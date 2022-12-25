from types import SimpleNamespace

class Object(SimpleNamespace):
    def __getattr__(self, name):
        return None
