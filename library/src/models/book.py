from dataclasses import asdict, dataclass
from typing import Final, cast
from src.pages import Destinations

from typing_extensions import Self

from src.database import connection, cursor

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
    def get_trending_books(self):
        # id, src, title, author
        # By number of active loans
        pass
    @classmethod
    def get_new_books(self):
        # id, src, title, author
        # By published date
        pass
    @classmethod
    def get_magazines_books(self):
        # id, src, title, author
        # By tag
        # find_by_tag_id
        pass
    @classmethod
    def get_classics_books(self):
        # id, src, title, author
        # By nymber of loans (lifetime)
        pass
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
        connection.commit()

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
    def search(cls, title: str, author: str, start : int) -> list[Self]:
        """Searches books."""
        payload = {"title": f"%{title}%", "author": f"%{author}%", "start":start}

        cursor.execute(
            """
            SELECT title, author, books.id, IFNULL(GROUP_CONCAT(name), '') from books 
            LEFT JOIN book_tags ON 
                books.id = book_tags.book_id
            LEFT JOIN tags ON
                book_tags.tag_id = tags.id
            WHERE
                title LIKE %(title)s
                AND author LIKE %(author)s
            GROUP BY books.id
            LIMIT 10 OFFSET %(start)s
            """,
            payload,
        )
        results = cursor.fetchall()
        return [{"primaryText":result[0], "secondaryText":result[1], "chips":result[3].strip().split(",") if result[3].strip() else [], "locator": (Destinations.bookInfo, result[2])} for result in results]  # type: ignore
    @classmethod
    def searchCount(cls, title: str, author: str) -> int:
        """Searches books."""
        payload = {"title": f"%{title}%", "author": f"%{author}%"}

        cursor.execute(
            """
            SELECT count(*) from books
            WHERE
                title LIKE %(title)s
                AND author LIKE %(author)s
            """,
            payload,
        )

        result = cursor.fetchone()
        return result[0]  # type: int

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
                title = %(title)s,
                author = %(author)s,
                cover_url = %(cover_url)s,
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
