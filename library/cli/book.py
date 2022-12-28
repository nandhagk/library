from click import group, option

from library.cli.book_copy import book_copy
from library.cli.book_tag import book_tag
from library.src.models.book import Book


@group()
def book() -> None:
    """Book management commands."""


@book.command()
@option("--title", required=True, help="Title of the book")
@option("--author", required=True, help="Author of the book")
@option("--cover-url", required=True, help="Cover URL of the book")
@option("--description", required=True, help="Description of the book")
def create(title: str, author: str, cover_url: str, description: str) -> None:
    """Creates a book."""
    book = Book.create(
        title=title,
        author=author,
        cover_url=cover_url,
        description=description,
        tag_ids=[],
    )

    print(book)


@book.command()
@option("--id", type=int, required=True, help="ID of the book")
def find_by_id(id: int) -> None:
    """Finds a book by its id."""
    book = Book.find_by_id(id)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@option("--id", type=int, required=True, help="ID of the book")
@option("--title", help="Title of the book")
def update(id: int, title: str | None) -> None:
    """Updates a book by its id."""
    book = Book.update(id, title=title)

    if book is None:
        print("Book not found!")
        return

    print(book)


@book.command()
@option("--id", type=int, required=True, help="ID of the book")
def delete(id: int) -> None:
    """Deletes a book by its id."""
    book = Book.delete(id)

    if book is None:
        print("Book not found!")
        return

    print(book)


book.add_command(book_copy)
book.add_command(book_tag)
