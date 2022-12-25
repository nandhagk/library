# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('../searchInput.css'))
from mypyguiplusultra.core import createRef

@styles
class Toggle(pyx.Component):
    def isActive(self):
        return 'off' not in self.bodyNode().state
    def toggle(self, *e):
        self.bodyNode().state.toggle('off')
        self.bodyNode().children[0].state.toggle('off')
    def onMount(self):
        self.bodyNode().on.click.subscribe(self.toggle)
    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'toggleContainer'}, "", pyx.pyx_factory.createElement("div", {'class': 'toggleCircle'}, ), "", )
@styles
class SwtichBoxInput(pyx.Component):
    def init(self):
        self.toggleContainer = createRef()

    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'inputContainer'}, "", pyx.pyx_factory.createElement("text", {'class': 'label'},  self.props['inputName']   , ), "", pyx.pyx_factory.createElement("div", {'class': 'switchBoxValueContainer'}, "",  *(  pyx.pyx_factory.createElement("span", {'class': 'switchBoxValue'},  value   , )  for value in self.props['options']['values'] ) , "", ), "", pyx.pyx_factory.createElement("div", {'class': 'switchBoxToggleContainer', 'ref': self.toggleContainer}, "",  *(  pyx.pyx_factory.createElement(Toggle, {'name': value}, )  for value in self.props['options']['values']) , "", ), "", )

    def getValue(self):
        return {
            toggle.props['name']:toggle.isActive() for toggle in self.toggleContainer().componentChildren
        }
