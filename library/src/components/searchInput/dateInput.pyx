import styles from './searchInput.css'
from mypyguiplusultra.core import createRef
from datetime import date
from src.customRenderWorkers import DateRenderWorker
@styles
class DateInput(pyx.Component):
    def init(self):
        self.input = createRef()
    def getValue(self):
        d = self.input().renderNode.renderWorker.calendarEditWidget.date()
        return date(d.year(), d.month(), d.day())
    def validate(self, *e):
        return True

    def onPaint(self):
        self.input().renderNode.renderWorker.setDate(self.props['options']['value'])

    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <div class="dateSelect" renderWorker={DateRenderWorker()} ref={self.input}/>
        </div>
