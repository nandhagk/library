from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict, cast

from library.database import connection, cursor
from library.models.book import Book


class CreateBookCopyPayload(TypedDict):
    book_id: int


class FindBookCopyPayload(TypedDict):
    id: int


class FindAvailableToLoanBookCopyPayload(TypedDict):
    book_id: int


class DeleteBookCopyPayload(TypedDict):
    id: int


@dataclass(frozen=True)
class BookCopy:
    id: int

    book_id: int

    def book(self) -> Book:
        return cast(Book, Book.find(self.id))

    @staticmethod
    def create(book_id: int) -> BookCopy:
        """Adds a copy of a book by its book id."""
        payload: CreateBookCopyPayload = {"book_id": book_id}

        cursor.execute(
            """
            INSERT INTO book_copies (book_id)
            VALUES (%(book_id)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        book_copy = cast(BookCopy, BookCopy.find(id))

        return book_copy

    @staticmethod
    def find(id: int, /) -> BookCopy | None:
        """Finds a copy of a book by its id."""
        payload: FindBookCopyPayload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM book_copies
            WHERE
                id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return BookCopy(*result)

    @staticmethod
    def find_available_to_loan(book_id: int, /) -> BookCopy | None:
        """Finds a copy of a book that is available to loan by its book id."""
        payload: FindAvailableToLoanBookCopyPayload = {"book_id": book_id}

        # https://stackoverflow.com/a/15389141
        cursor.execute(
            """
            SELECT book_copies.* FROM book_copies
            LEFT JOIN loans ON
                book_copies.id = loans.book_copy_id
                AND loans.status = 'active'
            WHERE
                book_id = %(book_id)s
                AND loans.book_copy_id IS NULL
            LIMIT 1
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return BookCopy(*result)

    @staticmethod
    def delete(id: int, /) -> BookCopy | None:
        """Deletes a book copy by its id."""
        book_copy = BookCopy.find(id)

        if book_copy is None:
            return

        payload: DeleteBookCopyPayload = {"id": book_copy.id}

        cursor.execute(
            """
            DELETE FROM book_copies
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return book_copy

    @staticmethod
    def init() -> None:
        """Initializes the book_copies table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS book_copies
            """
        )

        cursor.execute(
            """
            CREATE TABLE book_copies (
                id INT AUTO_INCREMENT,
                book_id INT NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (book_id)
                    REFERENCES books(id)
                    ON DELETE CASCADE
            )
            """
        )

        payload = [
            {"id": 1, "book_id": 1},
            {"id": 2, "book_id": 1},
            {"id": 3, "book_id": 2},
            {"id": 4, "book_id": 2},
            {"id": 5, "book_id": 2},
        ]

        cursor.executemany(
            """
            INSERT INTO book_copies (id, book_id)
            VALUES (%(id)s, %(book_id)s)
            """,
            payload,
        )

        connection.commit()
