# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

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
        return pyx.pyx_factory.createElement("div", {'class': 'container error'}, "", pyx.pyx_factory.createElement("text", {}, "PAGE NOT MADE", ), "", )

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
    def init(self):
        self.props['currentPage'].consequence = createRef(self.onPageChange)
        self.content = createRef()

    def onPageChange(self):
        self.content().unmount() # Remove the current one
        self.parentNode().appendChild(self) # Remount the content to the dom

    def body(self):
        cp = self.props['currentPage']() # Get the current page

        # if cp == Destinations.home:
        #     return <Home ref={self.content}/>
        if cp == Destinations.browse:
            return pyx.pyx_factory.createElement(Browse, {'ref': self.content})
        elif cp == Destinations.search:
            return pyx.pyx_factory.createElement(Search, {'ref': self.content})
        elif cp == Destinations.add:
            return pyx.pyx_factory.createElement(Add, {'ref': self.content})
        # elif cp == Destinations.edit:
        #     return <Edit ref={self.content}/>
        # elif cp == Destinations.loanInfo:
        #     return <LoanInfo ref={self.content}/>
        # elif cp == Destinations.bookInfo:
        #     return <BookInfo ref={self.content}/>
        # elif cp == Destinations.personInfo:
        #     return <PersonInfo ref={self.content}/>
        else:
            return pyx.pyx_factory.createElement(ErrorPage, {'ref': self.content})
