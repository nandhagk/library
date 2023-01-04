from mypyguiplusultra.core import createRef, createDependancy
from src.components import Toggle, SearchInput, SearchResult

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
                Name = SearchInput.Parameters.SingleLineText()            )
        elif self.searchFilter() == 'loans':
            return SearchInput.Parameters(
                BookID = SearchInput.Parameters.SingleLineText(),
                PersonID = SearchInput.Parameters.SingleLineText(),
                Status = SearchInput.Parameters.SwtichBoxInput(values=('Overdue', 'Active', 'Returned'))
            )
        else:
            print("INVALID SEARCHFILTER")


    def searchFilterChange(self):
        self.searchInput().updateParams(self.getParams())
        self.searchResult().clearResults()
        self.searchResult().bodyNode().renderNode.reflow().renderWorker.update()

    def body(self):
        return <div class="container">
            <Toggle searchFilter={self.searchFilter} items={['Loans', 'Books', 'People']}/>
            <SearchInput ref={self.searchInput} submitText={"Search"} submit={self.search} expect={self.getParams()}/>
            <SearchResult ref={self.searchResult} redirect={self.props['redirect']} />
        </div>

    def search(self, query):
        query['resource'] = self.searchFilter()
        self.searchResult().updateQuery(query)
