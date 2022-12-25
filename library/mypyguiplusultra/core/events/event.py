from threading import Event as Signal
from mypyguiplusultra.core.reference_handling.refs import createRef, Ref

class Event:
    ONGOING=0
    CANCELLED=1
    SUCCESSFUL=2

    def __init__(
        self,
        name,
        oneTimeOnly=False
    ):
        self.name = name
        self.__subscribers = set()
        self.__catchers = set()

        self.dontEmit = False
        self.oneTimeOnly = oneTimeOnly
        self.status = Event.ONGOING
        self.result = None

    def resolve(self, result : any):
        '''Resolves the promise'''
        if self.dontEmit:return

        if self.oneTimeOnly:
            self.dontEmit = True
            self.status = Event.SUCCESSFUL
            self.result = result

        for func in self.__subscribers:
            self._call_function(func, result)

        if self.oneTimeOnly:
            self.__subscribers.clear()
            self.__catchers.clear()
            del self.__subscribers
            del self.__catchers

    def cancel(self, reason : any):
        '''Cancels the promise'''
        if self.dontEmit:return

        if self.oneTimeOnly:
            self.dontEmit = True
            self.status = Event.CANCELLED
            self.result = result

        for func in self.__catchers:
            self._call_function(func, result)

        if self.oneTimeOnly:
            self.__subscribers.clear()
            self.__catchers.clear()
            del self.__subscribers
            del self.__catchers

    def _call_function(self, func : tuple, *args):
        '''Calls the function and sends the purity signal if required'''
        try:
            if isinstance(func, Ref):
                func()(*args)
            else:
                func(*args)
        except Exception as e:
            # import traceback
            # traceback.print_exc()
            print('Promise callback failure', e)


    def subscribe(self, callback : callable, weakify=True):
        '''
        Subscribes to the resolution of the promise
        Parameters:
            callback : (result)
            weakify : bool
                Set to true to make store a weak reference of the callback
        Returns:
            The same promise
        '''
        if weakify:callback = createRef(callback)

        if self.status == Event.ONGOING:
            self.__subscribers.add(callback)
            return self
        elif self.status == Event.SUCCESSFUL:
            self._call_function(callback, self.result)

        return self

    def catch(self, callback : callable, weakify=True):
        '''
        Subscribes to the cancellation of the promise
        Parameters:
            callback : (reason)
            weakify : bool
                Set to true to make store a weak reference of the callback
        Returns:
            The same promise
        '''
        if weakify:callback = createRef(callback)

        if self.status == Event.ONGOING:
            self.__catchers.add(callback)
            return self
        elif self.status == Event.SUCCESSFUL:
            self._call_function(callback, self.result)

        return self

    def wait(self):
        '''Holds the thread till the promise has been cancelled or resolved'''
        sig = Signal()
        self.subscribe(lambda r:sig.set(), weakify=False).catch(lambda r:sig.set(), weakify=False)
        sig.wait()
        return self.result
