from dataclasses import asdict, dataclass
from typing import Final, cast

from typing_extensions import Self

from library.database import connection, cursor

BOOKS: Final = [
    {"id": 1, "title": "Great Expectations"},
    {"id": 2, "title": "David Copperfield"},
]


@dataclass(frozen=True)
class Book:
    id: int
    title: str

    @classmethod
    def create(cls, title: str) -> Self:
        """Creates a book."""
        payload = {"title": title}

        cursor.execute(
            """
            INSERT INTO books (title)
            VALUES (%(title)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        book = cast(cls, cls.find(id))

        return book

    @classmethod
    def find(cls, id: int, /) -> Self | None:
        """Finds a book by its id."""
        payload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM books
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
    def find_by_tag_id(cls, tag_id: int, /) -> list[Self]:
        """Finds the books for a tag by its id."""
        payload = {"tag_id": tag_id}

        cursor.execute(
            """
            SELECT books.* from books
            JOIN book_tags ON
                books.id = book_tags.book_id
            WHERE
                book_tags.tag_id = %(tag_id)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def update(cls, id: int, /, title: str | None = None) -> Self | None:
        """Updates a book by its id."""
        book = cls.find(id)

        if book is None:
            return

        payload = asdict(book)

        if title is not None:
            payload["title"] = title

        cursor.execute(
            """
            UPDATE books
            SET
                title = %(title)s
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return cast(cls, cls.find(id))

    @classmethod
    def delete(cls, id: int, /) -> Self | None:
        """Deletes a book by its id."""
        book = cls.find(id)

        if book is None:
            return

        payload = {"id": book.id}

        cursor.execute(
            """
            DELETE FROM books
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return book

    @classmethod
    def init(cls) -> None:
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

        payload = BOOKS

        cursor.executemany(
            """
            INSERT INTO books (id, title)
            VALUES (%(id)s, %(title)s)
            """,
            payload,
        )
