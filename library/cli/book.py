from click import argument, group, option

from library.cli.book_copy import book_copy
from library.models.book import Book


@group()
def book() -> None:
    """Book management commands."""


@book.command()
@option("--title", required=True, help="Title of the book")
def create(title: str) -> None:
    """Creates a book."""
    book = Book.create(title=title)
    print(book)


@book.command()
@argument("id", type=int)
def find(id: int) -> None:
    """Finds a book by its id."""
    book = Book.find(id)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@argument("id", type=int)
@option("--title", help="Title of the book")
def update(id: int, title: str | None) -> None:
    """Updates a book by its id."""
    book = Book.update(id, title=title)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@argument("id", type=int)
def delete(id: int) -> None:
    """Deletes a book by its id."""
    book = Book.delete(id)

    if book is None:
        print("Book not found!")
        return

    print(book)


book.add_command(book_copy)
