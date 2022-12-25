# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

from mypyguiplusultra.core import createDependancy
from mypyguiplusultra.tools import createPyxApp
from mypyguiplusultra.pyx.stdlib import Body, defaultStyles

from .sidebar import Sidebar
from .pages import Content, Destinations

app = createPyxApp(
    globalStyleSheet=defaultStyles,
    minimumWindowSize=(500, 300),
    suppressQtWarnings=True
)

currentPage = createDependancy(Destinations.search)
    # Do the HOME PAGE

app.render(
    pyx.pyx_factory.createElement(Body, {}, "", pyx.pyx_factory.createElement(Sidebar, {'currentPage': currentPage}, ), "", pyx.pyx_factory.createElement(Content, {'currentPage': currentPage}, ), "", )
)

print('Execution finis ho gaya')
