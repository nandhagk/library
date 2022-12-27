import styles from 'personInfo.css'
from mypyguiplusultra.core import createRef
from src.components import SearchResult

def requestData(personId, callback):
    # TODO: SQL
    print("Requesting for", personId)
    callback({
        'personId' : '109678',
        'personName' : 'Shyam Prakash',
        'status' : 'Overdue'
    })

@styles
class PersonInfo(pyx.Component):
    def init(self):
        self.data = None
        self.refs = {
            'personName' : createRef(),
            'personId' : createRef(),
            'status' : createRef(),
        }
        self.searchResult = createRef()
        requestData(self.glob.data, self.handleData)

        # TODO: UI| Add delete and edit options

    def handleData(self, data):
        self.data = data
        
    def onMount(self): 
        # TODO: According to whether sql queries are asynchronous or not we might need to change this (maybe even move requesting data to onPaint if synchromous)
        for key in self.data:
            self.refs[key]().content = self.data[key]


    def onPaint(self):
        self.searchResult().updateQuery({
            'personId' : 123
        })

        # TODO: Think of the flow of how actually a new loan is made (cause right now the user has to remember the personId and bookId)
        # Maybe just keep some kind of validation that is done on unfocus that shows like person name and book name once id is put?

        # The edit pages will be easier than the info pages for sure

    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="infoContainer">
                    <text class="label">PersonID</text>
                    <text class="info" ref={self.refs['personId']}>Loading....</text>
                    <text class="label">PersonName</text>
                    <text class="info" ref={self.refs['personName']}>Loading....</text>
                    <text class="label">Staus</text>
                    <text class="info" ref={self.refs['status']}>Loading....</text>
                </div>        
            </div>
            <SearchResult ref={self.searchResult} heading="Loans:" redirect={self.props['redirect']} />
        </div>
