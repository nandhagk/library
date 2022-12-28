from dataclasses import asdict, dataclass
from typing import Final, cast

from typing_extensions import Self

from library.database import connection, cursor

BOOKS: Final = [
    {
        "id": 1,
        "title": "Great Expectations",
        "author": "Charles Dickens",
        "cover_url": "https://www.gamespot.com/a/uploads/original/1562/15626911/3002108-5033201-49-variant.jpg",
        "description": "Story book",
    },
    {
        "id": 2,
        "title": "David Copperfield",
        "author": "Charles Dickens",
        "cover_url": "https://www.gamespot.com/a/uploads/original/1562/15626911/3002108-5033201-49-variant.jpg",
        "description": "Story book",
    },
]


@dataclass(frozen=True)
class Book:
    id: int
    title: str
    author: str
    cover_url: str
    description: str

    @classmethod
    def create(
        cls,
        title: str,
        author: str,
        cover_url: str,
        description: str,
        tag_ids: list[int],
    ) -> Self:
        """Creates a book."""
        payload = {
            "title": title,
            "author": author,
            "cover_url": cover_url,
            "description": description,
        }

        cursor.execute(
            """
            INSERT INTO books (title, author, cover_url, description)
            VALUES (%(title)s, %(author)s, %(cover_url)s, %(description)s)
            """,
            payload,
        )

        id = cast(int, cursor.lastrowid)
        payload = [{"book_id": id, "tag_id": tag_id} for tag_id in tag_ids]

        cursor.executemany(
            """
            INSERT INTO book_tags (book_id, tag_id)
            VALUES (%(book_id)s, %(tag_id)s)
            """,
            payload,
        )

        connection.commit()

        book = cast(cls, cls.find_by_id(id))

        return book

    @classmethod
    def exists(cls, id: int, /) -> bool:
        return bool(cls.find_by_id(id))

    @classmethod
    def search(cls, title: str, author: str) -> list[Self]:
        """Searches books."""
        payload = {"title": f"%{title}%", "author": f"%{author}%"}

        cursor.execute(
            """
            SELECT * from books
            WHERE
                title ILIKE %(title)s
                OR author ILIKE %(author)s
            """,
            payload,
        )

        results = cursor.fetchall()
        return [cls(*result) for result in results]  # type: ignore

    @classmethod
    def find_by_id(cls, id: int, /) -> Self | None:
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
    def update(
        cls,
        id: int,
        /,
        title: str | None = None,
        author: str | None = None,
        cover_url: str | None = None,
        description: str | None = None,
    ) -> Self | None:
        """Updates a book by its id."""
        book = cls.find_by_id(id)

        if book is None:
            return

        payload = asdict(book)

        if title is not None:
            payload["title"] = title

        if author is not None:
            payload["author"] = author

        if cover_url is not None:
            payload["cover_url"] = cover_url

        if description is not None:
            payload["description"] = description

        cursor.execute(
            """
            UPDATE books
            SET
                title = %(title)s
                author = %(author)s
                cover_url = %(cover_url)s
                description = %(description)s
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return cast(cls, cls.find_by_id(id))

    @classmethod
    def delete(cls, id: int, /) -> Self | None:
        """Deletes a book by its id."""
        book = cls.find_by_id(id)

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
                author VARCHAR(255) NOT NULL,
                cover_Url TEXT NOT NULL,
                description VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        payload = BOOKS

        cursor.executemany(
            """
            INSERT INTO books (id, title, author, cover_url, description)
            VALUES (%(id)s, %(title)s, %(author)s, %(cover_url)s, %(description)s)
            """,
            payload,
        )
