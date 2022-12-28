import styles from './searchInput.css'
from src.customRenderWorkers import MultiLineRenderWorker
from mypyguiplusultra.core import createRef

@styles
class LongTextInput(pyx.Component):
    def init(self):
        self.input = createRef()
    def getValue(self):
        return self.input().content

    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <input class="long" ref={self.input} renderWorker={MultiLineRenderWorker()}>{self.props['options']['value']}</input>
        </div>

    def validate(self, *e):
        return True
