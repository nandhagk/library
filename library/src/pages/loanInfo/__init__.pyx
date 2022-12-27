import styles from 'loanInfo.css'
from mypyguiplusultra.core import createRef


def requestData(loanId, callback):
    # TODO: SQL
    print("Requesting for", loanId)
    callback({
        'loanId' : '109678',
        'bookId' : '123',
        'bookName' : "Harry Potter",
        'personName' : "Kaushik G Iyer",
        'personId' : '1234'
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
        }
        requestData(self.glob.data, self.handleData)

        # TODO: UI| Add delete and edit options

    def handleData(self, data):
        self.data = data

    def linkToBook(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.bookInfo, {'id' : self.data['bookId']})
    def linkToPerson(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.personInfo, {'id' : self.data['personId']})
        
    def onMount(self): # TODO: According to whether sql queries are asynchronous or not we might need to change this
        for key in self.data:
            self.refs[key]().content = self.data[key]

        self.refs['bookLink']().on.click.subscribe(self.linkToBook)
        self.refs['personLink']().on.click.subscribe(self.linkToPerson)

    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="infoContainer">
                    <text class="label">LoanID</text>
                    <text class="info" ref={self.refs['loanId']}>Loading....</text>
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
            
            </div>
        </div>
