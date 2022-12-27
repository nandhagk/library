import styles from 'bookInfo.css'
from mypyguiplusultra.core import createRef


def requestData(bookId, callback):
    # TODO: SQL
    print("Requesting for", bookId)
    callback({
        'title' : "Harry Potter and the Goblet of Fire",
        'author' : "J K Rowling",
        'bookId' : '108756',
        'description' : "Lorem ipsum dolor sit, amet consectetur adipisicing elit.Cumque repellat consequatur ipsum. Officiis ab eius asperiores, a suscipit beatae dolor!",
        'publisher' : "Ram Publishers",
        'publishedDate' : "20-10-2020",
        'pages' : '1433',
        'totalCopies' : "19",
        'activeCopies' : "7",
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
        
        requestData(self.glob.data, self.handleData)


        
    def handleData(self, data):
        self.data = data

    def onMount(self): # TODO: According to whether sql queries are asynchronous or not we might need to change this (maybe even move requesting data to onPaint if synchromous)
        for key in self.data:
            self.refs[key]().content = self.data[key]


        
    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="infoContainer">
                    <div class="leftBox">
                        <img source="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmmiS1QKc-r0rm8nNuTGqsADjbE1SZy4dRhQ&usqp=CAU"/>
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
            </div>
        </div>
