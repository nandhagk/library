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
# TODO NOW NOW:
# ASYNC!! SQL!! QUERIES!!

# TODO: Think of the flow of how actually a new loan is made (cause right now the user has to remember the personId and bookId)
# Maybe just keep some kind of validation that is done on unfocus that shows like person name and book name once id is put?


print('Execution finis ho gaya')
