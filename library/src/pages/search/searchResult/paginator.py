# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

from mypyguiplusultra.core import createRef, createDependancy
from math import ceil

@pyx.useStylesheet(
    """
    .container{
        position:absolute;
        right:1rem;
        bottom:1rem;
        display:inline;
    }
    span{
        font-size:0.65rem;
        font-weight:640;
    }
    svg{
        width:1rem;
        aspect-ratio:1rem;
        display:inline-block;
        margin-right:1rem;
        margin-left:-0.2rem;
    }
    svg:hover{
        opacity:0.5;
    }
    svg:inactive{
        opacity:0.4;
    }
    """
)
class Paginator(pyx.Component):
    def init(self):
        self.currentPage = 1
        self.totalPages = 1
        self.labelSpan = createRef()
        self.backSVG = createRef()
        self.frontSVG = createRef()

    def back(self, e):
        if self.currentPage == 1:return
        self.currentPage -= 1
        self.onPageChange()

    def front(self, e):
        if self.currentPage == self.totalPages:return
        self.currentPage += 1
        self.onPageChange()

    def updateActivity(self):
        if self.currentPage == 1:
            self.backSVG().state.add('inactive')
            self.backSVG().renderNode.renderWorker.setClickable(False)
        else:
            self.backSVG().state.remove('inactive')
            self.backSVG().renderNode.renderWorker.setClickable(True)

        if self.currentPage == self.totalPages:
            self.frontSVG().state.add('inactive')
            self.frontSVG().renderNode.renderWorker.setClickable(False)
        else:
            self.frontSVG().state.remove('inactive')
            self.frontSVG().renderNode.renderWorker.setClickable(True)


    def onMount(self):
        self.backSVG().on.click.subscribe(self.back)
        self.frontSVG().on.click.subscribe(self.front)
        self.backSVG().state.add('inactive', updateStyles=False)
        self.frontSVG().state.add('inactive', updateStyles=False)

    def onPageChange(self):
        self.labelSpan().content = self.getLabelText()
        self.updateActivity()
        self.labelSpan().renderNode.reflow().renderWorker.update()
        self.props['searchCommand']((self.currentPage - 1) * self.props['setSize'])

    def getLabelText(self):
        return f"Page {self.currentPage} of {self.totalPages}"

    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "", pyx.pyx_factory.createElement("span", {'ref': self.labelSpan},  self.getLabelText()   , ), "", pyx.pyx_factory.createElement("svg", {'ref': self.backSVG, 'src': Path(__file__).parent.joinpath(r"./back.svg").as_posix()}), "", pyx.pyx_factory.createElement("svg", {'ref': self.frontSVG, 'src': Path(__file__).parent.joinpath(r"./forward.svg").as_posix()}), "", )

    def setTotalPages(self, n):
        self.totalPages = ceil(n / self.props['setSize'])
        self.currentPage = 1
        self.onPageChange()
