# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

styles = mypyguiplusultra.objects.StyleSheet.fromPath(Path(__file__).parent.joinpath('browse.css'))
from PyQt6.QtWidgets import QGraphicsItem
@styles
class Browse(pyx.Component):
    def onClick(self, e):
        print(e[1].attrs['id'])

    def getBook(self, book):
        xs = pyx.pyx_factory.createElement("div", {'class': 'book', 'clickable': True, 'id': book['id']}, "", pyx.pyx_factory.createElement("img", {'source': book['src']}), "", pyx.pyx_factory.createElement("div", {'class': 'infoContainer', 'qflags': (QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren,)}, "", pyx.pyx_factory.createElement("text", {'class': 'name'},  book['title']   , ), "", pyx.pyx_factory.createElement("text", {'class': 'author'},  book['author']   , ), "", ), "", )

        xs.on.click.subscribe(self.onClick)

        return xs


    def hydrate(self, categories):
        return (( pyx.pyx_factory.createElement("div", {'class': 'section'}, "", pyx.pyx_factory.createElement("text", {'class': 'section-title'},  category   , ), "", pyx.pyx_factory.createElement("div", {'class': 'booksContainer'}, "",  *(self.getBook(book) for book in categories[category])   , "", ), "", )) for category in categories)

    def body(self):
        values = {"hot": [], "cold":[]}
        return pyx.pyx_factory.createElement("div", {'class': 'container'}, "",  *(self.hydrate( values ))   , "", )
