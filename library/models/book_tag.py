from __future__ import annotations

from dataclasses import dataclass
from typing import Final, cast

from library.database import connection, cursor
from library.models.book import Book
from library.models.tag import Tag

BOOK_TAGS: Final = [
    {"book_id": 1, "tag_id": 1},
    {"book_id": 1, "tag_id": 2},
    {"book_id": 2, "tag_id": 1},
]


@dataclass(frozen=True)
class BookTag:
    tag_id: int
    book_id: int

    def tag(self) -> Tag:
        return cast(Tag, Tag.find(self.tag_id))

    def book(self) -> Book:
        return cast(Book, Book.find(self.book_id))

    @staticmethod
    def create(book_id: int, tag_id: int) -> BookTag:
        """Creates a book tag."""
        payload = {"book_id": book_id, "tag_id": tag_id}

        cursor.execute(
            """
            INSERT INTO book_tags (book_id, tag_id)
            VALUES (%(book_id)s, %(tag_id)s)
            """,
            payload,
        )

        connection.commit()

        return cast(BookTag, BookTag.find(book_id=book_id, tag_id=tag_id))

    @staticmethod
    def find(book_id: int, tag_id: int) -> BookTag | None:
        """Finds a book tag by its book id and tag id."""
        payload = {"book_id": book_id, "tag_id": tag_id}

        cursor.execute(
            """
            SELECT * FROM book_tags
            WHERE
                book_id = %(book_id)s
                AND tag_id = %(tag_id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return

        return BookTag(*result)

    @staticmethod
    def delete(book_id: int, tag_id: int) -> BookTag | None:
        """Deletes a book tag by its book id and tag id."""
        book_tag = BookTag.find(book_id=book_id, tag_id=tag_id)

        if book_tag is None:
            return

        payload = {"book_id": book_id, "tag_id": tag_id}

        cursor.execute(
            """
            DELETE FROM book_tags
            WHERE
                book_id = %(book_id)s
                AND tag_id = %(tag_id)s
            """,
            payload,
        )

        connection.commit()

        return book_tag

    @staticmethod
    def init() -> None:
        """Initializes the book_tags table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS book_tags
            """
        )

        cursor.execute(
            """
            CREATE TABLE book_tags (
                tag_id INT NOT NULL,
                book_id INT NOT NULL,
                PRIMARY KEY (book_id, tag_id),
                FOREIGN KEY (book_id)
                    REFERENCES books(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (tag_id)
                    REFERENCES tags(id)
                    ON DELETE CASCADE
            )
            """
        )

        payload = BOOK_TAGS

        cursor.executemany(
            """
            INSERT INTO book_tags (book_id, tag_id)
            VALUES (%(book_id)s, %(tag_id)s)
            """,
            payload,
        )

        connection.commit()
