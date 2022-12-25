class EventEmitter:
    def __init__(self):
        self.__events = {}
        self.__setattr__ = self._setattr__ # Yes its kinda jank

    def __getattr__(self, name):
        return self.__events.get(name)

    def _setattr__(self, name, value): # NOTE: The typo is on purpose :)
        self.__events[name] = value
