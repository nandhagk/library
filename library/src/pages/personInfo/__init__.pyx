import styles from 'personInfo.css'
from mypyguiplusultra.core import createRef
from src.components import SearchResult

def deleteRecord(id):
    # TODO: SQL
    print("Deleting record")


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
        self.deleteButton = createRef()
        self.editButton = createRef()
        self.searchResult = createRef()
        requestData(self.glob.data, self.handleData)


    def handleData(self, data):
        self.data = data
        
    def onMount(self): 
        # TODO: According to whether sql queries are asynchronous or not we might need to change this (maybe even move requesting data to onPaint if synchromous)
        for key in self.data:
            self.refs[key]().content = self.data[key]
        self.deleteButton().on.click.subscribe(self.deleteRecord)
        self.editButton().on.click.subscribe(self.linkToEdit)

    def onPaint(self):
        self.searchResult().updateQuery({
            'personId' : 123
        })

    def linkToEdit(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.edit, {'type':'people', 'data' : self.data})
    def deleteRecord(self, *e):
        deleteRecord(self.data['personId'])
        from ..destinations import Destinations
        self.props['redirect'](Destinations.browse, {})

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
                <div class="absoluteBox">
                    <button class="delete" ref={self.deleteButton}>
                        <svg src="../../commonMedia/delete.svg"></svg>
                        <span class="del">Delete</span>
                    </button>
                    <button class="edit" ref={self.editButton}>
                        <svg src="../../commonMedia/edit.svg"></svg>
                        <span class="edi">Edit</span>
                    </button>
                </div>  
            </div>
            
           
             
            <SearchResult ref={self.searchResult} heading="Loans:" redirect={self.props['redirect']} />
        </div>
