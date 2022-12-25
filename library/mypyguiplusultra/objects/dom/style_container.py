from mypyguiplusultra.core import createRef

class StyleContainer:
    '''Contains the styles related to an element'''
    def __init__(self, node):
        self.element = createRef(node)
        self.scopedStyleSheet = None
        self.globalStyleSheet = None
        self.activeStyles = {}

    def __getattr__(self, name):
        return self.activeStyles.get(name)

    def computeStyles(self, notifyElement=True):
        styles = self.globalStyleSheet.getStyles(self.element())
        styles.update(self.scopedStyleSheet.getStyles(self.element()))
        # print(styles)
        if styles != self.activeStyles:
            self.activeStyles = styles
            if notifyElement:
                self.element()._onStyleChange()
            return True
        return False # No changes have been made to the true styles so return False
