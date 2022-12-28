from mypyguiplusultra.core import createDependancy, createRef
from src.components import Toggle, SearchInput

class Add(pyx.Component):
    def init(self):
        self.addFilter = createDependancy("loans", createRef(self.addFilterChange))

        self.searchInput = createRef()

    def getParams(self):
        if self.addFilter() == 'books':
            return SearchInput.Parameters(
                Title         = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()), # NOTE: Placeholder support has not been made yet
                Author        = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                CoverURL      = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()), # NOTE: Placeholder support has not been made yet
                Tags          = SearchInput.Parameters.ChipsInput(),
                Description   = SearchInput.Parameters.LongText(),
                Pages         = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip().isdigit()),
                TotalCopies   = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip().isdigit()),
                Publisher     = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                PublishedDate = SearchInput.Parameters.DateInput()
            )
        elif self.addFilter() == 'people':
            return SearchInput.Parameters(
                Name = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip())
            )
        elif self.addFilter() == 'loans':
            return SearchInput.Parameters(
                BookID     = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                PersonID   = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                IssuedDate = SearchInput.Parameters.DateInput(),
                DueDate    = SearchInput.Parameters.DateInput(),
            )
        elif self.addFilter() == 'tags':
            return SearchInput.Parameters(
                Name = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip())
            )
        else:
            print("INVALID ADDFILTER")

    def addFilterChange(self):
        self.searchInput().updateParams(self.getParams())

    def add(self, values):
        # TODO: SQL
        print("ADDING VALUES", values)
        id = "ID"
        # NOTE: Editing can basically just be a copy of this same page :)
        from ..destinations import Destinations
        if self.addFilter() == 'books':
            self.props['redirect'](Destinations.bookInfo, id)
        elif self.addFilter() == 'people':
            self.props['redirect'](Destinations.personInfo, id)
        elif self.addFilter() == 'loans':
            self.props['redirect'](Destinations.loanInfo, id)
        else:
            self.searchInput().updateParams(self.getParams())

    def body(self):
        return <div class="container">
            <Toggle searchFilter={self.addFilter} items={['Loans', 'Books', 'Tags', 'People']}/>
            <SearchInput ref={self.searchInput} submit={self.add} submitText={"Add"} expect={self.getParams()}/>
        </div>
