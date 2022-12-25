from mypyguiplusultra.core import createDependancy, createRef
from src.components import Toggle, SearchInput

class Add(pyx.Component):
    def init(self):
        self.addFilter = createDependancy("loans", createRef(self.addFilterChange))

        self.searchInput = createRef()

    def getParams(self):
        if self.addFilter() == 'books':
            return SearchInput.Parameters(
                Title       = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()), # NOTE: Placeholder support has not been made yet
                Author      = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                Tags        = SearchInput.Parameters.ChipsInput(),
                Description = SearchInput.Parameters.LongText()
            )
        elif self.addFilter() == 'people':
            return SearchInput.Parameters(
                Name = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                Status = SearchInput.Parameters.SwtichBoxInput(values=('Overdue', 'Lent', 'Returned', 'Damaged Before'))
            )
        elif self.addFilter() == 'loans':
            return SearchInput.Parameters(
                BookID = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                PersonID = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip()),
                Status = SearchInput.Parameters.SwtichBoxInput(values=('Overdue', 'Lent', 'Returned')),
                Date = SearchInput.Parameters.DateInput()
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
        # NOTE: Editing can basically just be a copy of this same page :)
        self.searchInput().updateParams(self.getParams())

    def body(self):
        return <div class="container">
            <Toggle searchFilter={self.addFilter} items={['Loans', 'Books', 'Tags', 'People']}/>
            <SearchInput ref={self.searchInput} submit={self.add} submitText={"Add"} expect={self.getParams()}/>
        </div>
