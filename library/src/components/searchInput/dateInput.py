# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('./searchInput.css'))
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
        return pyx.pyx_factory.createElement("div", {'class': 'inputContainer'}, "", pyx.pyx_factory.createElement("text", {'class': 'label'},  self.props['inputName']   , ), "", pyx.pyx_factory.createElement("div", {'class': 'dateSelect', 'renderWorker': DateRenderWorker(), 'ref': self.input}), "", )
