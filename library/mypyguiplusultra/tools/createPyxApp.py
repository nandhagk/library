from mypyguiplusultra import PYXApp
from mypyguiplusultra.objects.cssom import StyleSheet

def warningSuppressor(msg_type, msg_log_context, msg_string): # Suppress warnings :)
    pass


def createPyxApp(globalStyleSheet = StyleSheet(), minimumWindowSize=(None, None), suppressQtWarnings=True) -> PYXApp:
    app = PYXApp(globalStyleSheet, minimumWindowSize)
    app.windowProvider.on.ready.wait()
    if suppressQtWarnings:
        from PyQt6.QtCore import qInstallMessageHandler
        qInstallMessageHandler(warningSuppressor)
    return app
