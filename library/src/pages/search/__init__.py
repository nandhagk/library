# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

from mypyguiplusultra.core import createRef, createDependancy
from .searchResult import SearchResult
from src.components import Toggle, SearchInput

class Search(pyx.Component):
    def init(self):
        self.searchInput = createRef()
        self.searchResult = createRef()

        self.searchFilter = createDependancy("loans", createRef(self.searchFilterChange))

    def getParams(self):
        if self.searchFilter() == 'books':
            return SearchInput.Parameters(
                Title  = SearchInput.Parameters.SingleLineText(placeholder=''), # NOTE: Placeholder support has not been made yet
                Author = SearchInput.Parameters.SingleLineText(),
                Tags   = SearchInput.Parameters.ChipsInput()
            )
        elif self.searchFilter() == 'people':
            return SearchInput.Parameters(
                Name = SearchInput.Parameters.SingleLineText(),
                Status = SearchInput.Parameters.SwtichBoxInput(values=('Overdue', 'Lent', 'Returned', 'Damaged Before'))
            )
        elif self.searchFilter() == 'loans':
            return SearchInput.Parameters(
                BookID = SearchInput.Parameters.SingleLineText(),
                PersonID = SearchInput.Parameters.SingleLineText(),
                Status = SearchInput.Parameters.SwtichBoxInput(values=('Overdue', 'Lent', 'Returned'))
            )
        else:
            print("INVALID SEARCHFILTER")


    def searchFilterChange(self):
        self.searchInput().updateParams(self.getParams())

    def body(self):
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "", pyx.pyx_factory.createElement(Toggle, {'searchFilter': self.searchFilter, 'items': ['Loans', 'Books', 'People']}), "", pyx.pyx_factory.createElement(SearchInput, {'ref': self.searchInput, 'submitText': "Search", 'submit': self.search, 'expect': self.getParams()}), "", pyx.pyx_factory.createElement(SearchResult, {'ref': self.searchResult}), "", )

    def search(self, query):
        self.searchResult().updateQuery(query)
