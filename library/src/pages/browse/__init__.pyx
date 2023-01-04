import styles from 'browse.css'
from PyQt6.QtWidgets import QGraphicsItem
@styles
class Browse(pyx.Component):
    def onClick(self, e):
        from ..destinations import Destinations        
        self.props['redirect'](Destinations.bookInfo, e[1].attrs['bid'])

    def getBook(self, book):
        xs = <div class="book" clickable={True} bid={book.id}>
            <img source={book.cover_url} />
            <div class="infoContainer" qflags={(QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren,)}>
                <text class="name">{book.title[:16] + ("..." if book.title[16:] else '')}</text>
                <text class="author">{book.author[:17] + ("..." if book.author[17:] else '')}</text>
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
        from src.models.book import Book
        values = {"Trending": Book.get_trending_books(), "New": Book.get_new_books(), "Magazines":Book.get_magazines_books(), "Classics":Book.get_classics_books()}
        return <div class="container">
            {*(self.hydrate( values ))}
        </div>
