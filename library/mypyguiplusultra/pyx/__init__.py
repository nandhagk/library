from .component import Component
def useStylesheet(raw : str):
    from mypyguiplusultra.objects.cssom import StyleSheet
    return StyleSheet.fromString(raw)
