from mypyguiplusultra import PYXApp
from mypyguiplusultra.objects.cssom import StyleSheet
from mypyguiplusultra.core.util import Object
def warningSuppressor(msg_type, msg_log_context, msg_string): # Suppress warnings :)
    pass


def createPyxApp(globalStyleSheet = StyleSheet(), minimumWindowSize=(None, None), suppressQtWarnings=True, globalObject = Object()) -> PYXApp:
    from mypyguiplusultra.pyx.pyx_factory import setGlobalObject
    setGlobalObject(globalObject)
    
    app = PYXApp(globalStyleSheet, minimumWindowSize)
    app.windowProvider.on.ready.wait()
    if suppressQtWarnings:
        from PyQt6.QtCore import qInstallMessageHandler
        qInstallMessageHandler(warningSuppressor)
    return app
