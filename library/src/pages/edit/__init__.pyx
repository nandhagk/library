from mypyguiplusultra.core import createRef
from src.components import SearchInput

class Edit(pyx.Component):
    def getParams(self):
        print(self.glob['data'])
        if self.glob.data['type'] == 'books':
            return SearchInput.Parameters(
                BookID        = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['bookId']),
                Title         = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip(), value=self.glob['data']['data']['title']), # NOTE: Placeholder support has not been made yet
                Author        = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip(), value=self.glob['data']['data']['author']),
                CoverURL      = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip(), value=self.glob['data']['data']['coverURL']), # NOTE: Placeholder support has not been made yet
                Tags          = SearchInput.Parameters.ChipsInput(value=self.glob['data']['data']['tags']),
                Description   = SearchInput.Parameters.LongText(value=self.glob['data']['data']['description']),
                Pages         = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip().isdigit(), value=self.glob['data']['data']['pages']),
                TotalCopies   = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip().isdigit(), value=self.glob['data']['data']['totalCopies']),
                ActiveCopies  = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip().isdigit(), value=self.glob['data']['data']['activeCopies']),
                Publisher     = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip(), value=self.glob['data']['data']['publisher']),
                PublishedDate = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['publishedDate']),
            )
        elif self.glob.data['type'] == 'people':
            return SearchInput.Parameters(
                PersonID = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['personId']),
                Name = SearchInput.Parameters.SingleLineText(validate=lambda t:t.strip(), value=self.glob['data']['data']['personName'])
            )
        elif self.glob.data['type'] == 'loans':
            if self.glob['data']['data'].get('returnedDate') is not None:
                return SearchInput.Parameters(
                    LoanID     = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['loanId']),
                    BookID     = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['bookId']),
                    PersonID   = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['personId']),
                    IssuedDate = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['issuedDate']),
                    DueDate    = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['dueDate']),
                    ReturnedDate = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['returnedDate']),
                )
            else:
                return SearchInput.Parameters(
                    LoanID     = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['loanId']),
                    BookID     = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['bookId']),
                    PersonID   = SearchInput.Parameters.SingleLineText(disable=True, value=self.glob['data']['data']['personId']),
                    IssuedDate = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['issuedDate']),
                    DueDate    = SearchInput.Parameters.DateInput(value=self.glob['data']['data']['dueDate'])
                )

        else:
            print("INVALID ADDFILTER")

    def update(self, values):
        # TODO: SQL
        print("UPDATING VALUES", values)
        id = "ID"
        from ..destinations import Destinations
        if self.glob.data['type'] == 'books':
            self.props['redirect'](Destinations.bookInfo, id)
        elif self.glob.data['type'] == 'people':
            self.props['redirect'](Destinations.personInfo, id)
        elif self.glob.data['type'] == 'loans':
            self.props['redirect'](Destinations.loanInfo, id)
        else:
            self.searchInput().updateParams(self.getParams())

    def body(self):
        return <div class="container">
            <SearchInput submit={self.update} submitText={"Update"} expect={self.getParams()}/>
        </div>
