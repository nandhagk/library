import styles from './navItem.css'

from ..pages import Destinations

def getText(destination):
    if destination == Destinations.home:
        return "Home"
    elif destination == Destinations.browse:
        return "Browse"
    elif destination == Destinations.search:
        return "Search"
    elif destination == Destinations.add:
        return "Add"

def getSvgSource(destination):
    if destination == Destinations.home:
        return "./icons/home.svg"
    elif destination == Destinations.browse:
        return "./icons/library.svg"
    elif destination == Destinations.search:
        return "./icons/search.svg"
    elif destination == Destinations.add:
        return "./icons/add.svg"


@styles
class NavItem(pyx.Component):
    def onClick(self, e):
        self.props['callback'](self)

    def onMount(self):
        self.bodyNode().on.click.subscribe(self.onClick)
        if self.props.get('active'):self.bodyNode().state.add('active', updateStyles=False)

    def body(self):
        return <div class="container" clickable={not self.props.get('active', False)}>
            <svg src={getSvgSource(self.props['destination'])}/>
            <text>{getText(self.props['destination'])}</text>
        </div>
