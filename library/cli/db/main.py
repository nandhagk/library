from click import group

from library.cli.db.book import book
from library.database import cursor
from library.models.book import Book


@group()
def db() -> None:
    """Database management commands."""


@db.command()
def init() -> None:
    """Initializes the database."""
    cursor.execute(
        """
        DROP DATABASE IF EXISTS library
        """
    )

    cursor.execute(
        """
        CREATE DATABASE library
        """
    )

    cursor.execute(
        """
        USE library
        """
    )

    Book.init()

    print("Successfully initialized the database!")


db.add_command(book)
