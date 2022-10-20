from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TypedDict, cast

from library.database import connection, cursor


class CreateBookPayload(TypedDict):
    title: str


class FindBookPayload(TypedDict):
    id: int


class UpdateBookPayload(CreateBookPayload):
    id: int


class DeleteBookPayload(TypedDict):
    id: int


@dataclass
class Book:
    id: int
    title: str

    @staticmethod
    def create(title: str) -> Book:
        """Creates a new book."""
        payload: CreateBookPayload = {"title": title}

        cursor.execute(
            """
            INSERT INTO books (title)
            VALUES (%(title)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        book = cast(Book, Book.find(id))

        return book

    @staticmethod
    def find(id: int) -> Book | None:
        """Finds a book by its id."""
        payload: FindBookPayload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM books WHERE id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return Book(*result)

    @staticmethod
    def update(id: int, title: str | None = None) -> Book | None:
        """Updates a book by its id."""
        book = Book.find(id)

        if book is None:
            return

        payload = cast(UpdateBookPayload, asdict(book))

        if title is not None:
            payload["title"] = title

        cursor.execute(
            """
            UPDATE books SET title = %(title)s
            WHERE id = %(id)s
            """,
            payload,
        )

        connection.commit()

        book = cast(Book, Book.find(id))
        return book

    @staticmethod
    def delete(id: int) -> Book | None:
        """Deletes a book by its id."""
        book = Book.find(id)

        if book is None:
            return

        payload: DeleteBookPayload = {"id": book.id}

        cursor.execute(
            """
            DELETE FROM books WHERE id = %(id)s
            """,
            payload,
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
