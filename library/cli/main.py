from click import group

from library.src.cli.book import book
from library.src.cli.loan import loan
from library.src.cli.tag import tag
from library.src.cli.user import user
from library.src.database import cursor
from library.src.models.book import Book
from library.src.models.book_copy import BookCopy
from library.src.models.book_tag import BookTag
from library.src.models.loan import Loan
from library.src.models.tag import Tag
from library.src.models.user import User


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


main.add_command(book)
main.add_command(user)
main.add_command(loan)
main.add_command(tag)
