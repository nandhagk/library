# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

@pyx.useStylesheet(
    """
    """
)
class Home(pyx.Component):
    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "", )
