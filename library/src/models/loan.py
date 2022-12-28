from dataclasses import asdict, dataclass
from datetime import date
from typing import Final, Literal, TypeAlias, cast

from typing_extensions import Self

from library.database import connection, cursor
from library.src.models.book_copy import BookCopy
from library.src.models.user import User

LOANS: Final = [
    {"id": 1, "status": "active", "user_id": 1, "book_copy_id": 1, "returned_at": None},
    {
        "id": 2,
        "status": "returned",
        "user_id": 1,
        "book_copy_id": 2,
        "returned_at": "2022-12-28",
    },
    {"id": 3, "status": "active", "user_id": 2, "book_copy_id": 3, "returned_at": None},
    {
        "id": 4,
        "status": "returned",
        "user_id": 2,
        "book_copy_id": 4,
        "returned_at": "2022-12-28",
    },
]

LoanStatus: TypeAlias = Literal["active", "overdue", "returned"]


@dataclass(frozen=True)
class Loan:
    id: int
    status: LoanStatus

    user_id: int
    book_copy_id: int
    created_at: date
    returned_at: date | None = None

    def user(self) -> User:
        return cast(User, User.find_by_id(self.user_id))

    def book_copy(self) -> BookCopy:
        return cast(BookCopy, BookCopy.find_by_id(self.book_copy_id))

    @classmethod
    def create(cls, user_id: int, book_copy_id: int) -> Self:
        """Creates a loan."""
        payload = {
            "user_id": user_id,
            "book_copy_id": book_copy_id,
        }

        cursor.execute(
            """
            INSERT INTO loans (user_id, book_copy_id)
            VALUES (%(user_id)s, %(book_copy_id)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        loan = cast(cls, cls.find_by_id(id))

        return loan

    @classmethod
    def exists(cls, id: int, /) -> bool:
        return bool(cls.find_by_id(id))

    @classmethod
    def search(cls, book_id: int, user_id: int) -> list[Self]:
        """Searches loans."""
        payload = {"book_id": book_id, "user_id": user_id}

        cursor.execute(
            """
            SELECT loans.* from loans
            JOIN book_copies ON
                loans.book_copy_id = book_copies.id
            WHERE
                book_copies.book_id = %(book_id)s
                OR loans.user_id = %(user_id)s
            """,
            payload,
        )

        results = cursor.fetchall()
        return [cls(*result) for result in results]  # type: ignore

    @classmethod
    def find_by_id(cls, id: int, /) -> Self | None:
        """Finds a loan by its id."""
        payload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM loans
            WHERE
                id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return cls(*result)

    @classmethod
    def find_by_user_id(cls, user_id: int, /) -> list[Self]:
        """Finds the loans for a user by their id."""
        payload = {"user_id": user_id}

        cursor.execute(
            """
            SELECT * from loans
            WHERE
                user_id = %(user_id)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def find_by_book_copy_id(cls, book_copy_id: int, /) -> list[Self]:
        """Finds the loans for a copy of a book by its id."""
        payload = {"book_copy_id": book_copy_id}

        cursor.execute(
            """
            SELECT * from loans
            WHERE
                book_copy_id = %(book_copy_id)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def find_by_book_id(cls, book_id: int, /) -> list[Self]:
        """Finds the loans for a book by its id."""
        payload = {"book_id": book_id}

        cursor.execute(
            """
            SELECT loans.* from loans
            JOIN book_copies ON
                loans.book_copy_id = book_copies.id
            WHERE
                book_copies.book_id = %(book_id)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def update(
        cls,
        id: int,
        /,
        status: LoanStatus | None = None,
        returned_at: date | None = None,
    ) -> Self | None:
        """Updates a loan by its id."""
        loan = cls.find_by_id(id)

        if loan is None:
            return

        payload = asdict(loan)

        if status is not None:
            payload["status"] = status

        if returned_at is not None:
            payload["returned_at"] = returned_at.isoformat()

        cursor.execute(
            """
            UPDATE loans
            SET
                status = %(status)s
                returned_at = %(returned_at)s
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return cast(cls, cls.find_by_id(id))

    @classmethod
    def delete(cls, id: int, /) -> Self | None:
        """Deletes a loan by its id."""
        loan = cls.find_by_id(id)

        if loan is None:
            return

        payload = {"id": loan.id}

        cursor.execute(
            """
            DELETE FROM loans
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return loan

    @classmethod
    def init(cls) -> None:
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
                status ENUM('active', 'overdue', 'returned')
                    NOT NULL
                    DEFAULT 'active',
                user_id INT NOT NULL,
                book_copy_id INT NOT NULL,
                created_at DATE NOT NULL DEFAULT (CURRENT_DATE),
                returned_at DATE,
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

        payload = LOANS

        cursor.executemany(
            """
            INSERT INTO loans (id, status, user_id, book_copy_id, returned_at)
            VALUES (%(id)s, %(status)s, %(user_id)s, %(book_copy_id)s, %(returned_at)s)
            """,
            payload,
        )

        connection.commit()
