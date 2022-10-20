from click import group, option

from library.models.book_copy import BookCopy


@group("copy")
def book_copy() -> None:
    """Book copy management commands."""


@book_copy.command()
@option("--book-id", type=int, required=True, help="ID of the book")
def add(book_id: int) -> None:
    """Adds a copy of a book by its book id."""
    book_copy = BookCopy.create(book_id)
    print(book_copy)


@book_copy.command()
@option("--id", type=int, required=True, help="ID of the book copy")
def find(id: int) -> None:
    """Finds a copy of a book by its id."""
    book_copy = BookCopy.find(id)

    if book_copy is None:
        print("Book Copy not found!")
        return

    print(book_copy)


@book_copy.command()
@option("--id", type=int, required=True, help="ID of the book copy")
def delete(id: int) -> None:
    """Deletes a copy of a book by its id."""
    book_copy = BookCopy.delete(id)

    if book_copy is None:
        print("Book Copy not found!")
        return

    print(book_copy)
