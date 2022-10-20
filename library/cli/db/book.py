from click import group, option

from library.models.book import Book


@group()
def book() -> None:
    """Book management commands."""


@book.command()
@option("--title", required=True)
def create(title: str) -> None:
    """Creates a new book."""
    book = Book.create(title=title)
    print(book)


@book.command()
@option("--id", required=True, type=int)
def find(id: int) -> None:
    """Finds a book by its id."""
    book = Book.find(id)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@option("--id", required=True, type=int)
@option("--title")
def update(id: int, title: str | None) -> None:
    """Updates a book by its id."""
    book = Book.update(id, title=title)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@option("--id", required=True, type=int)
def delete(id: int) -> None:
    """Deletes a book by its id."""
    book = Book.delete(id)

    if book is None:
        print("Book not found!")
        return

    print(book)
