from dataclasses import asdict, dataclass
from datetime import date
from typing import Final, Literal, TypeAlias, cast

from src.database import connection, cursor
from src.models.book_copy import BookCopy
from src.models.user import User

from typing_extensions import Self

LOANS: Final = [
    {
        "id": 1,
        "status": "active",
        "user_id": 1,
        "book_copy_id": 1,
        "due_at": "2023-01-27",
        "created_at": "2023-01-27",
        "returned_at": None,
    },
    {
        "id": 2,
        "status": "returned",
        "user_id": 1,
        "book_copy_id": 2,
        "due_at": "2023-01-27",
        "created_at": "2023-01-27",
        "returned_at": "2022-12-28",
    },
    {
        "id": 3,
        "status": "active",
        "user_id": 2,
        "book_copy_id": 3,
        "due_at": "2023-01-27",
        "created_at": "2023-01-27",
        "returned_at": None,
    },
    {
        "id": 4,
        "status": "returned",
        "user_id": 2,
        "book_copy_id": 4,
        "due_at": "2023-01-27",
        "created_at": "2023-01-27",
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
    due_at: date
    returned_at: date | None = None

    def user(self) -> User:
        return cast(User, User.find_by_id(self.user_id))

    def book_copy(self) -> BookCopy:
        return cast(BookCopy, BookCopy.find_by_id(self.book_copy_id))

    @classmethod
    def create(
        cls,
        user_id: int,
        book_copy_id: int,
        created_at: date,
        due_at: date,
    ) -> Self:
        """Creates a loan."""
        payload = {
            "user_id": user_id,
            "book_copy_id": book_copy_id,
            "due_at": due_at,
            "created_at": created_at,
        }

        cursor.execute(
            """
            INSERT INTO loans (user_id, book_copy_id, created_at, due_at)
            VALUES (%(user_id)s, %(book_copy_id)s, %(created_at)s, %(due_at)s)
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
    def search(
        cls,
        book_id: int | None = None,
        user_id: int | None = None,
        statuses: list[LoanStatus] | None = None,
        start: int = 0,
    ) -> list[dict]:
        """Searches loans."""
        if statuses is None:
            statuses = []

        payload = {"start": start, "book_id": book_id, "user_id": user_id}

        status_where_clause = (
            f"""AND loans.status in ({','.join('"' + status + '"' for status in statuses)})"""
            if statuses
            else ""
        )

        query = f"""
        SELECT books.title, users.name, loans.status, loans.id from loans
        JOIN book_copies ON
            loans.book_copy_id = book_copies.id
        JOIN books ON
            book_copies.book_id = books.id
        JOIN users ON
            loans.user_id = users.id
        WHERE
            book_copies.book_id = IFNULL(%(book_id)s, book_copies.book_id)
            AND loans.user_id = IFNULL(%(user_id)s, loans.user_id)
            {status_where_clause}
        LIMIT 10
        OFFSET %(start)s
        """

        cursor.execute(query, payload)

        results = cursor.fetchall()

        if results is None:
            return []
        from src.pages.destinations import Destinations
        return [
            {
                "primaryText": user_name,
                "secondaryText": book_title,
                "chips": [loan_status],
                "locator": (Destinations.loanInfo, loan_id),
            }
            for book_title, user_name, loan_status, loan_id in results
        ]

    @classmethod
    def searchCount(
        cls,
        book_id: int | None = None,
        user_id: int | None = None,
        statuses: list[LoanStatus] | None = None,
    ) -> int:
        """Searches loans."""
        if statuses is None:
            statuses = []

        payload = {"book_id": book_id, "user_id": user_id}

        status_where_clause = (
            f"""AND loans.status in ({','.join('"' + status + '"' for status in statuses)})"""
            if statuses
            else ""
        )

        query = f"""
        SELECT count(*) from loans
        JOIN book_copies ON
            loans.book_copy_id = book_copies.id
        WHERE
            book_copies.book_id = IFNULL(%(book_id)s, book_copies.book_id)
            AND loans.user_id = IFNULL(%(user_id)s, loans.user_id)
            {status_where_clause}
        """

        cursor.execute(query, payload)

        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

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
    def find_for_ui(cls, id: int, /):
        payload = {"id": id}

        cursor.execute(
            """
            SELECT
                loans.id,
                books.id,
                books.title,
                users.name,
                users.id,
                loans.created_at,
                loans.returned_at,
                loans.due_at,
                loans.status
            from loans
            JOIN book_copies ON
                loans.book_copy_id = book_copies.id
            JOIN users ON
                loans.user_id = users.id
            JOIN books ON
                book_copies.book_id = books.id
            WHERE loans.id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()
        return result

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
    def update(
        cls,
        id: int,
        /,
        status: LoanStatus | None = None,
        due_at: date | None = None,
        created_at: date | None = None,
        returned_at: date | None = None,
    ) -> Self | None:
        """Updates a loan by its id."""
        loan = cls.find_by_id(id)

        if loan is None:
            return

        if (
            loan.returned_at is not None
            and loan.returned_at < loan.due_at
            and loan.status == "overdue"
        ):
            status = "returned"

        payload = asdict(loan)

        if status is not None:
            payload["status"] = status

        if due_at is not None:
            payload["due_at"] = due_at

        if created_at is not None:
            payload["created_at"] = created_at

        if returned_at is not None:
            payload["returned_at"] = returned_at
        cursor.execute(
            """
            UPDATE loans
            SET
                status = %(status)s,
                due_at = %(due_at)s,
                created_at = %(created_at)s,
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
                created_at DATE NOT NULL,
                due_at DATE NOT NULL,
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

        cursor.execute(
            """
            DROP EVENT IF EXISTS update_loan_status
            """
        )

        cursor.execute(
            """
            CREATE EVENT update_loan_status
            ON SCHEDULE EVERY 1 DAY
            DO
                UPDATE loans
                SET
                    status = 'overdue'
                WHERE
                    status = 'active'
                    AND due_at < IFNULL(returned_at, SYSDATE());
            """
        )

        payload = LOANS

        cursor.executemany(
            """
            INSERT INTO loans (
                id,
                status,
                user_id,
                book_copy_id,
                created_at,
                returned_at,
                due_at
            )
            VALUES (
                %(id)s,
                %(status)s,
                %(user_id)s,
                %(book_copy_id)s,
                %(created_at)s,
                %(returned_at)s,
                %(due_at)s
            )
            """,
            payload,
        )

        connection.commit()
