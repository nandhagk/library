from click import group, option

from library.models.book import Book, CreateBookPayload, UpdateBookPayload


@group()
def book() -> None:
    """Book management commands."""


@book.command()
@option("--title", required=True)
def create(title: str) -> None:
    """Creates a new book."""
    payload = CreateBookPayload(title=title)

    book = Book.create(payload)
    print(book)


@book.command()
@option("--id", required=True, type=int)
def find(id: int) -> None:
    """Finds a book by its id."""
    book = Book.find(id)
    print(book)


@book.command()
@option("--id", required=True, type=int)
@option("--title")
def update(id: int, title: str | None) -> None:
    """Delete a book by its id."""
    book = Book.find(id)

    if book is None:
        print("Book not found!")
        return

    payload: UpdateBookPayload = {}

    if title is not None:
        payload["title"] = title

    book.update(payload)
    print(book)


@book.command()
@option("--id", required=True, type=int)
def delete(id: int) -> None:
    """Delete a book by its id."""
    book = Book.find(id)

    if book is None:
        print("Book not found!")
        return

    book.delete()
    print(book)
