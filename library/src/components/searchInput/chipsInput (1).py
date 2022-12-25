# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('../searchInput.css'))
from mypyguiplusultra.core import createRef
from src.customRenderWorkers import InputRenderWorker

@styles
class ChipsInput(pyx.Component):
    def init(self):
        self.chipContainer = createRef()
        self.input = createRef()
        self.chips = set()

    def getValue(self):
        return self.chips

    def onKeyPress(self, e):
        if e.text().isspace():
            text = self.input().content
            self.input().renderNode.renderWorker.setText('')
            self.addChip(text.strip())

    def onMount(self):
        self.input().on.key.subscribe(self.onKeyPress)

    def removeChip(self, chip):
        self.chips.remove(chip.content.lower())
        chip.remove()

    def addChip(self, chipText):
        if not chipText or chipText.lower() in self.chips:return
        self.chips.add(chipText.lower())
        chip = pyx.pyx_factory.createElement("text", {'class': 'chip'},  chipText   , )
        chip.on.click.subscribe(lambda e:self.removeChip(chip), weakify=False)
        self.chipContainer().appendChild(chip)

    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'inputContainer'}, "", pyx.pyx_factory.createElement("text", {'class': 'label'},  self.props['inputName']   , ), "", pyx.pyx_factory.createElement("div", {'class': 'chipContainer', 'ref': self.chipContainer}, ), "", pyx.pyx_factory.createElement("input", {'class': 'chipSearch', 'ref': self.input, 'placeholder': self.props['options']['placeholder'], 'renderWorker': InputRenderWorker()}, ), "", )
