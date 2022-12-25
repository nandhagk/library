import styles from './searchInput.css'
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
        return <div class="toggleContainer">
            <div class="toggleCircle"></div>
        </div>
@styles
class SwtichBoxInput(pyx.Component):
    def init(self):
        self.toggleContainer = createRef()

    def body(self):
        return <div class="inputContainer">
            <text class="label">{self.props['inputName']}</text>
            <div class="switchBoxValueContainer">
                {*( <span class="switchBoxValue">{value}</span> for value in self.props['options']['values'] )}
            </div>
            <div class="switchBoxToggleContainer" ref={self.toggleContainer}>
                {*( <Toggle name={value}></Toggle> for value in self.props['options']['values'])}
            </div>
        </div>
    def validate(self, *e):
        return True
    def getValue(self):
        return {
            toggle.props['name']:toggle.isActive() for toggle in self.toggleContainer().componentChildren
        }
