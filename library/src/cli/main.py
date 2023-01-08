from click import group
from src.database import cursor
from src.models.book import Book
from src.models.book_copy import BookCopy
from src.models.book_tag import BookTag
from src.models.loan import Loan
from src.models.tag import Tag
from src.models.user import User


@group()
def main() -> None:
    """Launches the app."""


@main.command()
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

    Tag.init()
    Book.init()
    User.init()
    BookTag.init()
    BookCopy.init()
    Loan.init()

    print("Successfully initialized the database!")
