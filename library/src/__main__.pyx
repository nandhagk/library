from mypyguiplusultra.core import createDependancy, createRef
from mypyguiplusultra.core.util import Object
from mypyguiplusultra.tools import createPyxApp
from mypyguiplusultra.pyx.stdlib import Body, defaultStyles

from .sidebar import Sidebar
from .pages import Content, Destinations

glob = Object()

app = createPyxApp(
    globalStyleSheet=defaultStyles,
    minimumWindowSize=(500, 300),
    suppressQtWarnings=True,
    globalObject = glob
)
# TODO: Window Icon

sidebar = createRef()
glob.currentPage = createDependancy(Destinations.browse)

app.render(
    <Body>
        <Sidebar ref={sidebar}></Sidebar>
        <Content sidebar={sidebar}></Content>
    </Body>
)

print('Execution finis ho gaya')
