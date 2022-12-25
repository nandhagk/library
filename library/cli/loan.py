from click import group, option

from library.src.models.book_copy import BookCopy
from library.src.models.loan import Loan


@group()
def loan() -> None:
    """Loan management commands."""


@loan.command()
@option("--book-id", required=True, type=int, help="ID of the book")
@option("--user-id", required=True, type=int, help="ID of the user")
def issue(book_id: int, user_id: int) -> None:
    """Loans a book to a user by their ids."""
    book_copy = BookCopy.find_available_to_loan(book_id)

    if book_copy is None:
        print("No copy of book is available to loan!")
        return

    loan = Loan.create(user_id=user_id, book_copy_id=book_copy.id)
    print(loan)


@loan.command("return")
@option("--id", type=int, required=True, help="ID of the loan")
def return_(id: int) -> None:
    """Return a loaned book by its loan id."""
    loan = Loan.update(id, status="returned")

    if loan is None:
        print("Loan not found!")
        return

    print(loan)
