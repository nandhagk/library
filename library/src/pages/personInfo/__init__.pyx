import styles from 'personInfo.css'
from mypyguiplusultra.core import createRef
from src.components import SearchResult
def deleteRecord(id):
    from src.models.user import User
    User.delete(id)


def requestData(personId, callback):
    from src.models.user import User
    user = User.find_by_id(personId)
    callback({
        'personId' : str(user.id),
        'personName' : user.name,
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
        for key in self.data:
            self.refs[key]().content = self.data[key]
        self.deleteButton().on.click.subscribe(self.deleteRecord)
        self.editButton().on.click.subscribe(self.linkToEdit)

    def onPaint(self):
        self.searchResult().updateQuery({
            'resource':'loans',
            'PersonID' : self.data['personId'],
            'status' : {},
            'BookID' : ''
        })

    def linkToEdit(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.edit, {'type':'people', 'data' : self.data})
    def deleteRecord(self, *e):
        if not self.parentNode().renderNode.windowProvider().confirm("Are you sure you want to delete the user record?"):return
        deleteRecord(self.data['personId'])
        from ..destinations import Destinations
        self.parentNode().renderNode.windowProvider().inform("User record was successfully deleted!")
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
