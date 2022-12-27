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
# ellipse text overflow | honestly kinda doable (would look nice in the cards)

# Fix image bug | idk when this bug even happens (feature moment?)

# Make the info pages

# Make the edit pages

# TODO:
# BookInfo

# Edit pages for each info (just the same as the add pages)

# personInfo, loanInfo must contain links :) (to eachother and to also to the book)

# Maybe start with loanInfo first

# Then do person info (basically just shows name and a ResultContainer of all the loans in recent order)

# After that do the edit pages

# Once the edit pages are done just finish of the bookInfo (yes I know its a pain in the ass but still finish it)

print('Execution finis ho gaya')
