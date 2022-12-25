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
        return <div class="container">
            <Toggle searchFilter={self.searchFilter} items={['Loans', 'Books', 'People']}/>
            <SearchInput ref={self.searchInput} submitText={"Search"} submit={self.search} expect={self.getParams()}/>
            <SearchResult ref={self.searchResult}/>
        </div>

    def search(self, query):
        self.searchResult().updateQuery(query)
