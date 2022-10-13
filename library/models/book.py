from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import cast

from library.database import connection, cursor


@dataclass
class CreateBookPayload:
    title: str


@dataclass
class Book:
    id: int
    title: str

    @staticmethod
    def create(payload: CreateBookPayload) -> Book:
        """Creates a new book."""
        data = asdict(payload)

        cursor.execute(
            """
            INSERT INTO books (title)
            VALUES (%(title)s)
            """,
            data,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        book = cast(Book, Book.find(id))

        return book

    @staticmethod
    def find(id: int) -> Book | None:
        """Finds a book by its id."""
        cursor.execute(
            """
            SELECT * FROM books WHERE id = %(id)s
            """,
            {"id": id},
        )

        result = cursor.fetchone()

        if result is None:
            return

        return Book(*result)

    @staticmethod
    def delete(id: int) -> Book | None:
        """Deletes a book by its id."""
        book = Book.find(id)

        if book is None:
            return

        cursor.execute(
            """
            DELETE FROM books WHERE id = %(id)s
            """,
            {"id": id},
        )

        connection.commit()

        return book

    @staticmethod
    def init() -> None:
        """Initializes the books table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS books
            """
        )

        cursor.execute(
            """
            CREATE TABLE books (
                id INT AUTO_INCREMENT,
                title VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )
