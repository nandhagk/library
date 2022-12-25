# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('../searchInput.css'))
from .chipsInput import ChipsInput
from .singleLineInput import SingleLineInput
from .switchBoxInput import SwtichBoxInput
from mypyguiplusultra.core import createRef
from mypyguiplusultra.tools.renderWorkers import TextRenderWorker

@styles
class SearchInput(pyx.Component):
    class Parameters:
        _SingleLineText = 0
        _ChipsInput     = 1
        _SwtichBoxInput  = 2

        @staticmethod
        def SingleLineText(placeholder=''):
            return (SearchInput.Parameters._SingleLineText, {
                'placeholder':placeholder
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

        def __init__(self, **params):
            self.params = params
        def __repr__(self):
            return repr(self.params)

    def getValue(self):
        return {component.props['inputName']:component.getValue() for component in self.bodyNode().componentChildren}

    def submitInput(self, e):
        value = self.getValue()
        self.props['submit'](value)

    def init(self):
        self.submit = createRef()

    def onMount(self):
        self.submit().on.click.subscribe(self.submitInput)

    def updateParams(self, params):
        self.props['expect'] = params
        container = self.bodyNode()
        for child in container.children:
            child.remove(_relayout=False, _removeFromParentList=False)
        container.children.clear()


        for element in (self.createInput(k, v) for k, v in self.props['expect'].params.items()):
            container.appendChild(element, _relayout=False)
        container.appendChild( pyx.pyx_factory.createElement("button", {'ref': self.submit, 'renderWorker': TextRenderWorker()}, "Submit", ), _relayout=False)
        container.reflow().update()


    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "",  *(self.createInput(k, v) for k, v in self.props['expect'].params.items())   , "", pyx.pyx_factory.createElement("button", {'ref': self.submit, 'renderWorker': TextRenderWorker()}, "Submit", ), "", )

    def createInput(self, inputName, inputType):
        if inputType[0] == SearchInput.Parameters._SingleLineText:
            return pyx.pyx_factory.createElement(SingleLineInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._ChipsInput:
            return pyx.pyx_factory.createElement(ChipsInput, {'inputName': inputName, 'options': inputType[1]})
        elif inputType[0] == SearchInput.Parameters._SwtichBoxInput:
            return pyx.pyx_factory.createElement(SwtichBoxInput, {'inputName': inputName, 'options': inputType[1]})
        else:
            print("INVALID INPUT TYPE")
