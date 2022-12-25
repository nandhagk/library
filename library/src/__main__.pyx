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
    <Body>
        <Sidebar currentPage={currentPage}></Sidebar>
        <Content currentPage={currentPage}></Content>
    </Body>
)

print('Execution finis ho gaya')
