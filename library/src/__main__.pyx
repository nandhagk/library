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
# TODO: Chips were overflowing
# TODO: Some height problems when secondary text is empty
# TODO: Clear results when switching tabs
# TODO: Show loans in book info
# TODO: Add a title for edit page
# TODO: Paginator when 0 entries bugs out
# TODO: Paginator show number of entries

sidebar = createRef()
glob.currentPage = createDependancy(Destinations.browse)

app.render(
    <Body>
        <Sidebar ref={sidebar}></Sidebar>
        <Content sidebar={sidebar}></Content>
    </Body>
)

print('Execution finis ho gaya')
