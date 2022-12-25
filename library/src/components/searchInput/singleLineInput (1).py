# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('../searchInput.css'))
from src.customRenderWorkers import InputRenderWorker
from mypyguiplusultra.core import createRef

@styles
class SingleLineInput(pyx.Component):
    def init(self):
        self.input = createRef()
    def getValue(self):
        return self.input().content
    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'inputContainer'}, "", pyx.pyx_factory.createElement("text", {'class': 'label'},  self.props['inputName']   , ), "", pyx.pyx_factory.createElement("input", {'ref': self.input, 'renderWorker': InputRenderWorker(), 'placeholder': self.props['options']['placeholder']}, ), "", )
