# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('./navItem.css'))

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
        return pyx.pyx_factory.createElement("div", {'class': 'container', 'clickable': not self.props.get('active', False)}, "", pyx.pyx_factory.createElement("svg", {'src': Path(__file__).parent.joinpath(getSvgSource(self.props['destination'])).as_posix()}), "", pyx.pyx_factory.createElement("text", {},  getText(self.props['destination'])   , ), "", )
