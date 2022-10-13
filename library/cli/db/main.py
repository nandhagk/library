from click import group

from library.cli.db.book import book
from library.models.book import Book


@group()
def db() -> None:
    """Database management commands."""


@db.command()
def init() -> None:
    """Initializes the database."""
    Book.init()

    print("Successfully initialized the database!")


db.add_command(book)
