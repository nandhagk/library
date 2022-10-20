from click import group

from library.cli.book import book
from library.cli.loan import loan
from library.cli.user import user
from library.database import cursor
from library.models.book import Book
from library.models.book_copy import BookCopy
from library.models.loan import Loan
from library.models.user import User


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

    Book.init()
    User.init()
    BookCopy.init()
    Loan.init()

    print("Successfully initialized the database!")


main.add_command(book)
main.add_command(user)
main.add_command(loan)
