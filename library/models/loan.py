from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict, cast

from library.database import connection, cursor
from library.models.book_copy import BookCopy
from library.models.user import User


class CreateLoanPayload(TypedDict):
    user_id: int
    book_copy_id: int


class FindLoanPayload(TypedDict):
    id: int


class DeleteLoanPayload(TypedDict):
    id: int


@dataclass(frozen=True)
class Loan:
    id: int

    user_id: int
    book_copy_id: int

    def user(self) -> User:
        return cast(User, User.find(self.user_id))

    def book_copy(self) -> BookCopy:
        return cast(BookCopy, BookCopy.find(self.book_copy_id))

    @staticmethod
    def create(user_id: int, book_copy_id: int) -> Loan:
        """Creates a loan."""
        payload: CreateLoanPayload = {"user_id": user_id, "book_copy_id": book_copy_id}

        cursor.execute(
            """
            INSERT INTO loans (user_id, book_copy_id)
            VALUES (%(user_id)s, %(book_copy_id)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        loan = cast(Loan, Loan.find(id))

        return loan

    @staticmethod
    def find(id: int, /) -> Loan | None:
        """Finds a loan by its id."""
        payload: FindLoanPayload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM loans WHERE id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return Loan(*result)

    @staticmethod
    def delete(id: int, /) -> Loan | None:
        """Deletes a loan by its id."""
        loan = Loan.find(id)

        if loan is None:
            return

        payload: DeleteLoanPayload = {"id": loan.id}

        cursor.execute(
            """
            DELETE FROM loans WHERE id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return loan

    @staticmethod
    def init() -> None:
        """Initializes the loans table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS loans
            """
        )

        cursor.execute(
            """
            CREATE TABLE loans (
                id INT AUTO_INCREMENT,
                user_id INT NOT NULL,
                book_copy_id INT NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (book_copy_id)
                    REFERENCES book_copies(id)
                    ON DELETE CASCADE
            )
            """
        )

        payload = [
            {"id": 1, "user_id": 1, "book_copy_id": 2},
            {"id": 2, "user_id": 2, "book_copy_id": 4},
        ]

        cursor.executemany(
            """
            INSERT INTO loans (id, user_id, book_copy_id)
            VALUES (%(id)s,  %(user_id)s, %(book_copy_id)s)
            """,
            payload,
        )

        connection.commit()
