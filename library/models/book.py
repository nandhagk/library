from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TypedDict, cast

from library.database import connection, cursor


@dataclass
class CreateBookPayload:
    title: str


class UpdateBookPayload(TypedDict, total=False):
    title: str


@dataclass
class Book:
    id: int
    title: str

    def delete(self) -> None:
        """Deletes the book."""
        cursor.execute(
            """
            DELETE FROM books WHERE id = %(id)s
            """,
            {"id": self.id},
        )

        connection.commit()

    def update(self, payload: UpdateBookPayload) -> None:
        """Updates the book."""
        data = asdict(self) | payload

        cursor.execute(
            """
            UPDATE books SET title = %(title)s
            WHERE id = %(id)s
            """,
            data,
        )

        connection.commit()

        for field, value in data.items():
            setattr(self, field, value)

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
