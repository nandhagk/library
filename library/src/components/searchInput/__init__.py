# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('./searchInput.css'))
from .chipsInput import ChipsInput
from .singleLineInput import SingleLineInput
from .switchBoxInput import SwtichBoxInput
from .longTextInput import LongTextInput
from .dateInput import DateInput
from mypyguiplusultra.core import createRef
from mypyguiplusultra.tools.renderWorkers import TextRenderWorker

@styles
class SearchInput(pyx.Component):
    class Parameters:
        _SingleLineText = 0
        _ChipsInput     = 1
        _SwtichBoxInput = 2
        _LongText       = 3
        _DateInput      = 4

        @staticmethod
        def DateInput():
            return (SearchInput.Parameters._DateInput, {})
        @staticmethod
        def SingleLineText(placeholder='', validate=lambda t:True):
            return (SearchInput.Parameters._SingleLineText, {
                'placeholder':placeholder,
                'validate':validate
            })
        @staticmethod
        def ChipsInput(placeholder=''):
            return (SearchInput.Parameters._ChipsInput, {
                'placeholder':placeholder
            })
        @staticmethod
        def SwtichBoxInput(values=()):
            return (SearchInput.Parameters._SwtichBoxInput, {
                'values':values
            })
        @staticmethod
        def LongText():
            return (SearchInput.Parameters._LongText, {

            })

        def __init__(self, **params):
            self.params = params
        def __repr__(self):
            return repr(self.params)

    def getValue(self):
        value = {}
        invalid = False
        for component in self.bodyNode().componentChildren:
            if not component.validate():invalid=True
            if invalid:continue
            value[component.props['inputName']] = component.getValue()
        if invalid:return None
        return value

    def submitInput(self, e):
        value = self.getValue()
        if value is None:return
        self.props['submit'](value)

    def init(self):
        self.submit = createRef()

    def onMount(self):
        self.submit().on.click.subscribe(self.submitInput)

    def updateParams(self, params):
        self.props['expect'] = params
        container = self.bodyNode()
        for component in container.componentChildren:
            component.unmount(_notifyNode=False)
        container.componentChildren.clear()
        for child in container.children:
            child.remove(_relayout=False, _removeFromParentList=False)
        container.children.clear()


        for element in (self.createInput(k, v) for k, v in self.props['expect'].params.items()):
            container.appendChild(element, _relayout=False)
        container.appendChild( pyx.pyx_factory.createElement("button", {'ref': self.submit, 'renderWorker': TextRenderWorker()},  self.props['submitText']   , ), _relayout=False)
        self.onMount()
        xs = container.renderNode.reflow()
        for child in container.children:
            child.renderNode.renderWorker.paint()
        xs.renderWorker.update()
    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "",  *(self.createInput(k, v) for k, v in self.props['expect'].params.items())   , "", pyx.pyx_factory.createElement("button", {'ref': self.submit, 'renderWorker': TextRenderWorker()},  self.props['submitText']   , ), "", )

    def createInput(self, inputName, inputType):
        if inputType[0] == SearchInput.Parameters._SingleLineText:
            return pyx.pyx_factory.createElement(SingleLineInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._ChipsInput:
            return pyx.pyx_factory.createElement(ChipsInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._SwtichBoxInput:
            return pyx.pyx_factory.createElement(SwtichBoxInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._LongText:
            return pyx.pyx_factory.createElement(LongTextInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._DateInput:
            return pyx.pyx_factory.createElement(DateInput, {'inputName': inputName, 'options': inputType[1]})
        else:
            print("INVALID INPUT TYPE")
