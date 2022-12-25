import styles from 'browse.css'
from PyQt6.QtWidgets import QGraphicsItem
@styles
class Browse(pyx.Component):
    def onClick(self, e):
        print(e[1].attrs['id'])

    def getBook(self, book):
        xs = <div class="book" clickable={True} id={book['id']}>
            <img source={book['src']} />
            <div class="infoContainer" qflags={(QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren,)}>
                <text class="name">{book['title']}</text>
                <text class="author">{book['author']}</text>
            </div>
        </div>

        xs.on.click.subscribe(self.onClick)

        return xs


    def hydrate(self, categories):
        return (( <div class="section">
                <text class="section-title">{category}</text>
                <div class="booksContainer">
                    {*(self.getBook(book) for book in categories[category])}
                </div>
            </div>) for category in categories)

    def body(self):
        values = {"hot": [], "magazines":[]}
        return <div class="container">
            {*(self.hydrate( values ))}
        </div>
