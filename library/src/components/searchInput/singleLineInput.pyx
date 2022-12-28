import styles from './searchInput.css'
from src.customRenderWorkers import InputRenderWorker
from mypyguiplusultra.core import createRef

@styles
class SingleLineInput(pyx.Component):
    def init(self):
        self.input = createRef()
    def getValue(self):
        return self.input().content

    def validate(self, *e):
        if self.props['options']['validate'](self.input().content):
            self.input().state.remove('invalid')
            return True
        self.input().state.add('invalid')
        return False

    def onPaint(self):
        if self.props['options']['disable']:
            self.input().state.add('disabled')
            self.input().renderNode.renderWorker.setEnabled(False)

    def onMount(self):
        self.input().on.unfocus.subscribe(self.validate)
    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <input ref={self.input} renderWorker={InputRenderWorker()} placeholder={self.props['options']['placeholder']}>{self.props['options']['value']}</input>
        </div>
