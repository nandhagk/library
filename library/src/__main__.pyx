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

sidebar = createRef()
glob.currentPage = createDependancy(Destinations.loanInfo)

app.render(
    <Body>
        <Sidebar ref={sidebar}></Sidebar>
        <Content sidebar={sidebar}></Content>
    </Body>
)
# TODO:
# Make the edit pages

# TODO:
# Edit pages for each info (just the same as the add pages) (Or should we make it the same as info page?)

# After that do the edit pages

print('Execution finis ho gaya')
