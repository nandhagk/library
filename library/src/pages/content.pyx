from mypyguiplusultra.core import createRef

from .destinations import Destinations

from .home import Home
from .browse import Browse
from .search import Search
from .add import Add
from .edit import Edit
from .loanInfo import LoanInfo
from .bookInfo import BookInfo
from .personInfo import PersonInfo


@pyx.useStylesheet(
    """
    .error{
        background-color: red;
    }
    text{
        font-size:7.5%;
        margin:3rem;
        text-overflow:nowrap;
    }
    """
)
class ErrorPage(pyx.Component):
    def body(self):
        return <div class="container error">
            <text>PAGE NOT MADE</text>
        </div>

@pyx.useStylesheet(
    """
    .container{
        height: 100vh;
        background-color:#1e1e1e;
        display: inline-block;
        overflow-y:scroll;
    }
    """
)
class Content(pyx.Component):
    def setTitle(self):
        title = ""
        cp = self.glob.currentPage()
        # if cp == Destinations.home:
        #     title = "Library - Home"
        if cp == Destinations.browse:
            title = "Library - Browse"
        elif cp == Destinations.search:
            title = "Library - Search"
        elif cp == Destinations.add:
            title = "Library - Add"
        elif cp == Destinations.edit:
            title = "Library - Edit"
        elif cp == Destinations.loanInfo:
            title = "Library - Loan Info"
        elif cp == Destinations.bookInfo:
            title = "Library - Book Info"
        elif cp == Destinations.personInfo:
            title = "Library - Person Info"
        self.parentNode().renderNode.windowProvider().setTitle(title)
    def init(self):
        self.glob.currentPage.consequence = createRef(self.onPageChange)
        self.content = createRef()
        self.glob.data = None

    def onPageChange(self):
        
        self.content().unmount() # Remove the current one
        self.parentNode().appendChild(self) # Remount the content to the dom

    def onPaint(self):
        self.setTitle()

    def redirect(self, page, data):
        # Redirect is only called for pages not accesable by the sidebar
        self.glob.data = data
        self.props.sidebar().deactivate()
        if page != Destinations.browse:
            return self.glob.currentPage.set(page) # Yes it is ugly. But it works
        self.props.sidebar().navigate(self.props.sidebar().bodyNode().componentChildren[0])

    def body(self):
        cp = self.glob.currentPage() # Get the current page

        # if cp == Destinations.home:
        #     return <Home ref={self.content}/>
        if cp == Destinations.browse:
            return <Browse ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.search:
            return <Search ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.add:
            return <Add ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.edit:
            return <Edit ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.loanInfo:
            return <LoanInfo ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.bookInfo:
            return <BookInfo ref={self.content} redirect={self.redirect}/>
        elif cp == Destinations.personInfo:
            return <PersonInfo ref={self.content} redirect={self.redirect}/>
        else:
            return <ErrorPage ref={self.content} redirect={self.redirect}/>
