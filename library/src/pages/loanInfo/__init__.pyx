import styles from 'loanInfo.css'
from mypyguiplusultra.core import createRef
from datetime import date

def deleteRecord(id):
    from src.models.loan import Loan
    Loan.delete(id)

def returnLoan(id):
    from src.models.loan import Loan
    Loan.update(id, status="returned", returned_at=date.today())

def requestData(loanId, callback):
    from src.models.loan import Loan
    res = Loan.find_for_ui(loanId)
    callback({
        'loanId' : str(res[0]),
        'bookId' : str(res[1]),
        'bookName' : res[2],
        'personName' : res[3],
        'personId' : str(res[4]),
        'issuedDate' : res[5].strftime("%d-%b-%Y"),
        'returnedDate' : res[6].strftime("%d-%b-%Y") if res[6] is not None else None,
        'dueDate' : res[7].strftime("%d-%b-%Y"),
        'status' : res[8],
    })

@styles
class LoanInfo(pyx.Component):
    def init(self):
        self.data = None
        self.refs = {
            'loanId' : createRef(),
            'bookId' : createRef(),
            'bookName' : createRef(),
            'personName' : createRef(),
            'personId' : createRef(),
            'bookLink' : createRef(),
            'personLink' : createRef(),
            'dueDate' : createRef(),
            'returnedDate' : createRef(),
            'status' : createRef(),
            'issuedDate' : createRef()
        }
        self.deleteButton = createRef()
        self.returnButton = createRef()
        self.editButton = createRef()
        self.returnDateLabel = createRef()
        requestData(self.glob.data, self.handleData)

    def handleData(self, data):
        self.data = data

    def linkToBook(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.bookInfo, self.data['bookId'])
    def returnLoan(self, *e):
        if not self.parentNode().renderNode.windowProvider().confirm("Are you sure you want to return the loan?"):return
        from ..destinations import Destinations
        returnLoan(self.data['loanId'])
        self.props['redirect'](Destinations.loanInfo, self.data['loanId'])

    def linkToPerson(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.personInfo, self.data['personId'])
    def linkToEdit(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.edit, {'type':'loans', 'data' : self.data})
    def deleteRecord(self, *e):
        if not self.parentNode().renderNode.windowProvider().confirm("Are you sure you want to delete the loan record?"):return
        deleteRecord(self.data['loanId'])
        from ..destinations import Destinations
        self.parentNode().renderNode.windowProvider().inform("Loan record was successfully deleted!")
        self.props['redirect'](Destinations.browse, {})

        
    def onMount(self):
        for key in self.data:
            self.refs[key]().content = self.data[key]

        self.refs['bookLink']().on.click.subscribe(self.linkToBook)
        self.refs['personLink']().on.click.subscribe(self.linkToPerson)

        self.deleteButton().on.click.subscribe(self.deleteRecord)
        self.editButton().on.click.subscribe(self.linkToEdit)
        self.returnButton().on.click.subscribe(self.returnLoan)

    def onPaint(self):
        if self.data.get('returnedDate') is not None:
            self.returnButton().remove()
        else:
            self.refs['returnedDate']().remove()
            self.returnDateLabel().remove()
        


    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="infoContainer">
                    <text class="label">LoanID</text>
                    <text class="info" ref={self.refs['loanId']}>Loading....</text>
                    <text class="label">Issued Date</text>
                    <text class="info" ref={self.refs['issuedDate']}>Loading....</text>
                    <text class="label">Due Date</text>
                    <text class="info" ref={self.refs['dueDate']}>Loading....</text>
                    <text class="label" ref={self.returnDateLabel}>Returned Date</text>
                    <text class="info" ref={self.refs['returnedDate']}>Loading....</text>
                    <text class="label">Status</text>
                    <text class="info" ref={self.refs['status']}>Loading....</text>
                </div>
                <div class="infoContainer">
                    <text class="label">BookID</text>
                    <text class="info" ref={self.refs['bookId']}>Loading....</text>
                    <text class="label">Book Name</text>
                    <text class="info" ref={self.refs['bookName']}>Loading....</text>
                    <text class="link" clickable={True} ref={self.refs['bookLink']}>More Info</text>
                </div>
                <div class="infoContainer">
                    <text class="label">PersonID</text>
                    <text class="info" ref={self.refs['personId']}>Loading....</text>
                    <text class="label">PersonName</text>
                    <text class="info" ref={self.refs['personName']}>Loading....</text>
                    <text class="link" clickable={True} ref={self.refs['personLink']}>More Info</text>
                </div>
                <div class="absoluteBox">
                    <button class="delete" ref={self.deleteButton}>
                        <svg src="../../commonMedia/delete.svg"></svg>
                        <span class="del">Delete</span>
                    </button>
                    <button class="edit" ref={self.editButton}>
                        <svg src="../../commonMedia/edit.svg"></svg>
                        <span class="edi">Edit</span>
                    </button>
                    <button class="return" ref={self.returnButton}>
                        <svg src="return.svg"></svg>
                        <span class="ret">Return</span>
                    </button>
                </div>
            
            </div>
        </div>
