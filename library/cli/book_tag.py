from click import group, option

from library.src.models.book_tag import BookTag


@group("tag")
def book_tag() -> None:
    """Book tag management commands."""


@book_tag.command()
@option("--book-id", type=int, required=True, help="ID of the book")
@option("--tag-id", type=int, required=True, help="ID of the tag")
def add(book_id: int, tag_id: int) -> None:
    """Adds a tag to a book by their ids."""
    book_tag = BookTag.create(book_id=book_id, tag_id=tag_id)
    print(book_tag)


@book_tag.command()
@option("--book-id", type=int, required=True, help="ID of the book")
@option("--tag-id", type=int, required=True, help="ID of the tag")
def remove(book_id: int, tag_id: int) -> None:
    """Removes a tag from a book by their ids."""
    book_tag = BookTag.delete(book_id=book_id, tag_id=tag_id)

    if book_tag is None:
        print("Book Tag not found!")
        return

    print(book_tag)
