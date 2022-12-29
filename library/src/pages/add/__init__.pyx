from mypyguiplusultra.core import createDependancy, createRef
from src.components import Toggle, SearchInput
from src.models.book import Book
from src.models.book_copy import BookCopy
from src.models.loan import Loan
from src.models.user import User
from src.models.tag import Tag


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
                BookID     = SearchInput.Parameters.SingleLineText(validate=lambda t:BookCopy.find_available_to_loan(t) is not None),
                PersonID   = SearchInput.Parameters.SingleLineText(validate=lambda t:User.exists(t)),
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
        # TODO: SQL Later
        # NOTE: Editing can basically just be a copy of this same page :)
        from ..destinations import Destinations
        if self.addFilter() == 'books':
            # TODO: Enter tags
            # TODO: ALl the other shit
            # {'Title': 'sdf', 'Author': 'sdf', 'CoverURL': 'sdf', 'Tags': set(), 'Description': ' dfsdf', 'Pages': '123', 'TotalCopies': '2', 'Publisher': 'dsf', 'PublishedDate': (28, 12, 2022)}
            book = Book.create(values['Title'], values['Author'], values['CoverURL'], values['Description'], [])   
            self.parentNode().renderNode.windowProvider().inform("Book record has been created!", "Information")
            self.props['redirect'](Destinations.bookInfo, book.id)
        elif self.addFilter() == 'people':
            user = User.create(values['Name'])
            self.parentNode().renderNode.windowProvider().inform("User record has been created!", "Information")
            self.props['redirect'](Destinations.personInfo, user.id)
        elif self.addFilter() == 'loans':
            book_copy = BookCopy.find_available_to_loan(values['BookID'])
            loan = Loan.create(values['PersonID'], book_copy.id, values['IssuedDate'], values['DueDate'])
            self.parentNode().renderNode.windowProvider().inform("Loan record has been created!", "Information")
            self.props['redirect'](Destinations.loanInfo, loan.id)
        elif self.addFilter() == 'tags':
            tag = Tag.create(values['Name'])
            self.parentNode().renderNode.windowProvider().inform("Tag record has been created!", "Information")
            self.searchInput().updateParams(self.getParams())
        else:
            self.searchInput().updateParams(self.getParams())

    def body(self):
        return <div class="container">
            <Toggle searchFilter={self.addFilter} items={['Loans', 'Books', 'Tags', 'People']}/>
            <SearchInput ref={self.searchInput} submit={self.add} submitText={"Add"} expect={self.getParams()}/>
        </div>
