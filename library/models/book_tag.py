from dataclasses import dataclass
from typing import Final, cast

from typing_extensions import Self

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

    @classmethod
    def create(cls, book_id: int, tag_id: int) -> Self:
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

        return cast(cls, cls.find(book_id=book_id, tag_id=tag_id))

    @classmethod
    def find(cls, book_id: int, tag_id: int) -> Self | None:
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

        return cls(*result)

    @classmethod
    def delete(cls, book_id: int, tag_id: int) -> Self | None:
        """Deletes a book tag by its book id and tag id."""
        book_tag = cls.find(book_id=book_id, tag_id=tag_id)

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

    @classmethod
    def init(cls) -> None:
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
