import styles from 'bookInfo.css'

def requestData(bookId, callback):
    # TODO: SQL
    print("Requesting for", bookId)
    callback({
        
    })

@styles
class BookInfo(pyx.Component):
    def init(self):
        self.data = None
        requestData(self.glob.data, self.handleData)

        
    def handleData(self, data):
        self.data = data


        
    def body(self):
        return <div class="container">
            <div class="allContainer">
                <div class="leftBox">
                    <img source="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmmiS1QKc-r0rm8nNuTGqsADjbE1SZy4dRhQ&usqp=CAU"/>
                    <span class="title">Title</span>
                    <span class="author">Author</span>
                </div>
                <div class="rightBox">
                    <span class="description"></span>
                </div>
            
            </div>
        </div>
