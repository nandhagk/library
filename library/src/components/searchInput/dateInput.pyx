import styles from './searchInput.css'
from mypyguiplusultra.core import createRef

from src.customRenderWorkers import DateRenderWorker
@styles
class DateInput(pyx.Component):
    def init(self):
        self.input = createRef()
    def getValue(self):
        date = self.input().renderNode.renderWorker.calendarEditWidget.date()
        return (date.day(), date.month(), date.year())
    def validate(self, *e):
        return True

    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <div class="dateSelect" renderWorker={DateRenderWorker()} ref={self.input}/>
        </div>
