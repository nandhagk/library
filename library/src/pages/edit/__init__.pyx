from mypyguiplusultra.core import createRef
from src.components import SearchInput

from src.models.book import Book
from src.models.loan import Loan
from src.models.user import User

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
        print("UPDATING VALUES", values)
        from ..destinations import Destinations
        if self.glob.data['type'] == 'books':
            Book.update(self.glob['data']['data']['bookId'], title=values['Title'], author=values['Author'], cover_url=values['CoverURL'],description= values['Description'])
            self.props['redirect'](Destinations.bookInfo, self.glob['data']['data']['bookId'])
        elif self.glob.data['type'] == 'people':
            User.update(self.glob['data']['data']['personId'], name=values['Name'])
            self.props['redirect'](Destinations.personInfo, self.glob['data']['data']['personId'])
        elif self.glob.data['type'] == 'loans':

            Loan.update(self.glob['data']['data']['loanId'], created_at=values['IssuedDate'], due_at=values['DueDate'], returned_at=values.get('returnedDate'))
            self.props['redirect'](Destinations.loanInfo, self.glob['data']['data']['loanId'])
        else:
            self.searchInput().updateParams(self.getParams())

    def body(self):
        return <div class="container">
            <SearchInput submit={self.update} submitText={"Update"} expect={self.getParams()}/>
        </div>
