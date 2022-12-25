from .node import RenderNode
from .layout_helper import LayoutHelper
from mypyguiplusultra.core.util import Object
from mypyguiplusultra.objects.cssom import css_enums

class RootRenderNode(RenderNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.set(self)

    def setHeirarchy(self):
        for child in self.domNode().children:
            child.renderNode.setHeirarchy(self, self)

    def layout(self, *args, **kwargs):
        '''Positions every element'''
        width, height = self.renderWorker.getWindowSize()
        styleHints = LayoutHelper.getStyleHints(self)
        styleHints.width = width
        styleHints.height = height
        LayoutHelper.layoutNode(self, styleHints, contentSizeCalculator=LayoutHelper.getBoxContentSize)
