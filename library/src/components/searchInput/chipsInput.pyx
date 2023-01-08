import styles from './searchInput.css'
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
    def validate(self, *e):
        return True

    def onKeyPress(self, e):
        if e[0].text() == '\r':
            # TODO NOW: Only add tag if the tag exists (we need to have validation for tags)
            text = self.input().content
            
            self.input().renderNode.renderWorker.setText('')
            self.addChip(text.strip())

    def onMount(self):
        self.input().on.key.subscribe(self.onKeyPress)

    def removeChip(self, chip):
        self.chips.remove(chip.content.lower())
        chip.remove()

    def onPaint(self):
        for chip in self.props['options']['value']:
            self.addChip(chip)

    def addChip(self, chipText):
        chipText = chipText.lower()
        if not chipText or chipText in self.chips:return
        if not (self.props['options']['validate'](chipText)):
            self.parentNode().renderNode.windowProvider().inform("Tag does not exist!")
            return
        self.chips.add(chipText.lower())
        chip = <text class="chip">{chipText.title()}</text>
        chip.on.click.subscribe(lambda e:self.removeChip(chip), weakify=False)
        self.chipContainer().appendChild(chip)

    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <div class="chipContainer" ref={self.chipContainer}></div>
            <input class="chipSearch" ref={self.input} placeholder={self.props['options']['placeholder']} renderWorker={InputRenderWorker()}></input>
        </div>
