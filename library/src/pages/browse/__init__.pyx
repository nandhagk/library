import styles from 'browse.css'
from PyQt6.QtWidgets import QGraphicsItem
from textwrap import shorten
@styles
class Browse(pyx.Component):
    def onClick(self, e):
        from ..destinations import Destinations        
        self.props['redirect'](Destinations.bookInfo, e[1].attrs['bid'])

    def getBook(self, book):
        xs = <div class="book" clickable={True} bid={book.id}>
            <img source={book.cover_url} />
            <div class="infoContainer" qflags={(QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren,)}>
                <text class="name">{shorten(book.title, 17, placeholder="...")}</text>
                <text class="author">{shorten(book.author, 16, placeholder="...")}</text>
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
        values = {"Trending": Book.get_trending_books(), "New": Book.get_new_books(), "Comics":Book.get_magazines_books(), "Classics":Book.get_classics_books()}

        return <div class="container">
            {*(self.hydrate( values ))}
        </div>
