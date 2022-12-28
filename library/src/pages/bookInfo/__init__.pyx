import styles from 'bookInfo.css'
from mypyguiplusultra.core import createRef

def deleteRecord(id):
    # TODO: SQL
    print("Deleting record")
def requestData(bookId, callback):
    # TODO: SQL
    print("Requesting for", bookId)
    callback({
        'title' : "Harry Potter and the Goblet of Fire",
        'author' : "J K Rowling",
        'bookId' : '108756',
        'description' : "Lorem ipsum dolor sit, amet consectetur adipisicing elit.Cumque repellat consequatur ipsum. Officiis ab eius asperiores, a suscipit beatae dolor!",
        'publisher' : "Ram Publishers",
        'publishedDate' : "20-Oct-2020",
        'pages' : '1433',
        'totalCopies' : "19",
        'tags' : ['horror', 'mystery', 'fantasy', 'detective'],
        'activeCopies' : "7",
        'coverURL' : 'https://lh3.googleusercontent.com/AtjQKneFRMLZyLUSeLvDkYpB0Zj8ltEoA5LUhqEpT60hvWaaMSlmE-dQ_mkpdEdcSkDe_jx4ImKKfhGl=w544-h544-l90-rj'
    })
    

@styles
class BookInfo(pyx.Component):
    def init(self):
        self.data = None
        self.refs = {
            'title' : createRef(),
            'author' : createRef(),
            'description' : createRef(),
            'bookId' : createRef(),
            'description' : createRef(),
            'publisher' : createRef(),
            'publishedDate' : createRef(),
            'totalCopies' : createRef(),
            'pages' : createRef(),

            'activeCopies' : createRef(),
        }
        self.coverImg = createRef()
        self.deleteButton = createRef()
        self.chipsViewer = createRef()
        self.editButton = createRef()
        
        requestData(self.glob.data, self.handleData)

    def linkToEdit(self, *e):
        from ..destinations import Destinations
        self.props['redirect'](Destinations.edit, {'type':'books', 'data' : self.data})

    def deleteRecord(self, *e):
        deleteRecord(self.data['bookId'])
        from ..destinations import Destinations
        self.props['redirect'](Destinations.browse, {})
        
    def handleData(self, data):
        self.data = data

    def onMount(self): 
        # TODO NOW: According to whether sql queries are asynchronous or not we might need to change this (maybe even move requesting data to onPaint if synchromous)
        for key in self.data:
            if key in {'tags', 'coverURL'}:                
                continue
            self.refs[key]().content = self.data[key]

        cv = self.chipsViewer()
        for chip in self.data['tags']:
            cv.appendChild( <text class="chip">{chip}</text>, _link=False)
        
        


        self.deleteButton().on.click.subscribe(self.deleteRecord)
        self.editButton().on.click.subscribe(self.linkToEdit)

    def onPaint(self):
        self.coverImg().renderNode.renderWorker.setImageSource(self.data['coverURL'])
        self.coverImg().renderNode.renderWorker.loadImageFromSource()

        
    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="infoContainer">
                    <div class="leftBox">
                        <img ref={self.coverImg} source="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmmiS1QKc-r0rm8nNuTGqsADjbE1SZy4dRhQ&usqp=CAU"/>
                    </div>
                    <div class="rightBox">
                        <text class="label">Title</text>
                        <text class="info" ref={self.refs['title']}>Loading...</text>
                        <text class="label">Author</text>
                        <text class="info" ref={self.refs['author']}>Loading...</text>
                        <text class="label">BookID</text>
                        <text class="info" ref={self.refs['bookId']}>Loading...</text>
                    </div>
                </div>
                <div class="infoContainer chipsViewer" ref={self.chipsViewer}>
                    <text class="label">Tags</text>
                </div>
                <div class="infoContainer">
                    <text class="label">Description</text>
                    <text class="info" ref={self.refs['description']}>Loading....</text>
                </div>
                <div class="infoContainer">
                    <text class="label">Pages</text>
                    <text class="info" ref={self.refs['pages']}>Loading....</text>
                    <text class="label">Total Copies</text>
                    <text class="info" ref={self.refs['totalCopies']}>Loading....</text>
                    <text class="label">Active Copies</text>
                    <text class="info" ref={self.refs['activeCopies']}>Loading....</text>
                </div>  
                <div class="infoContainer">
                    <text class="label">Publisher</text>
                    <text class="info" ref={self.refs['publisher']}>Loading....</text>
                    <text class="label">Published Date</text>
                    <text class="info" ref={self.refs['publishedDate']}>Loading....</text>
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
        </div>
