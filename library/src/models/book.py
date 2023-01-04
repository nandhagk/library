from dataclasses import asdict, dataclass
from datetime import date
from typing import Final, cast

from src.database import connection, cursor
from src.pages import Destinations
from typing_extensions import Self

BOOKS: Final = [
    {
        "id": 1,
        "title": "Great Expectations",
        "author": "Charles Dickens",
        "cover_url": "",
        "description": "Story book",
        "publisher": "Penguin Book House",
        "published_at": date.today(),
        "pages": 250,
    },
    {
        "id": 2,
        "title": "David Copperfield",
        "author": "Charles Dickens",
        "cover_url": "",
        "description": "Story book",
        "publisher": "Penguin Book House",
        "published_at": date.today(),
        "pages": 250,
    },
]


@dataclass(frozen=True)
class Book:
    id: int
    title: str
    author: str
    cover_url: str
    description: str
    publisher: str
    published_at: date
    pages: int

    @classmethod
    def get_trending_books(cls):
        """Get trending books."""
        cursor.execute(
            """
            SELECT books.* from books
            JOIN book_copies ON
                book_copies.book_id = books.id
            JOIN loans ON
                loans.book_copy_id = book_copies.id
                AND loans.status = 'active'
            GROUP BY
                books.id
            ORDER BY
                COUNT(loans.id)
            LIMIT 10
            """
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def get_new_books(cls):
        """Get new books."""
        cursor.execute(
            """
            SELECT * from books
            ORDER BY
                published_at DESC
            LIMIT 10
            """
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def get_magazines_books(cls) -> list[Self]:
        """Gets magazine books."""
        return cls.find_by_tag_id(3)

    @classmethod
    def get_classics_books(cls):
        """Get classic books."""
        cursor.execute(
            """
            SELECT books.* from books
            JOIN book_copies ON
                book_copies.book_id = books.id
            JOIN loans ON
                loans.book_copy_id = book_copies.id
            GROUP BY
                books.id
            ORDER BY
                COUNT(loans.id)
            LIMIT 10
            """
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def create(
        cls,
        title: str,
        author: str,
        cover_url: str,
        description: str,
        publisher: str,
        published_at: date,
        pages: int,
        copies: int,
        tags: list[str],
    ) -> int:
        """Creates a book."""
        payload = {
            "title": title,
            "author": author,
            "cover_url": cover_url,
            "description": description,
            "publisher": publisher,
            "published_at": published_at,
            "pages": pages,
        }

        cursor.execute(
            """
            INSERT INTO books (
                title,
                author,
                cover_url,
                description,
                publisher,
                published_at,
                pages
            )
            VALUES (
                %(title)s,
                %(author)s,
                %(cover_url)s,
                %(description)s,
                %(publisher)s,
                %(published_at)s,
                %(pages)s
            )
            """,
            payload,
        )

        id = cast(int, cursor.lastrowid)
        payload = [{"book_id": id} for _ in range(copies)]

        cursor.executemany(
            """
            INSERT INTO book_copies (book_id)
            VALUES (%(book_id)s)
            """,
            payload,
        )

        payload = [{"book_id": id, "tag": tag} for tag in tags]

        cursor.executemany(
            """
            INSERT INTO book_tags (book_id, tag_id)
            VALUES (%(book_id)s, (SELECT tags.id FROM tags WHERE tags.name = %(tag)s))
            """,
            payload,
        )

        connection.commit()
        return id

    @classmethod
    def exists(cls, id: int, /) -> bool:
        return bool(cls.find_by_id(id))

    @classmethod
    def search(
        cls,
        title: str = "",
        author: str = "",
        tags: list[str] | None = None,
        start: int = 0,
    ) -> list[dict]:
        """Searches books."""
        if tags is None:
            tags = []

        tag_search_clause = (
            (
                "HAVING "
                + "\n AND ".join(
                    f'IFNULL(GROUP_CONCAT(tags.name), "") LIKE "%{tag}%"'
                    for tag in tags
                )
            )
            if tags
            else ""
        )

        payload = {"title": f"%{title}%", "author": f"%{author}%", "start": start}

        query = f"""
        SELECT
            books.id,
            books.title,
            books.author,
            GROUP_CONCAT(tags.name)
        from books
        LEFT JOIN book_tags ON
            books.id = book_tags.book_id
        LEFT JOIN tags ON
            book_tags.tag_id = tags.id
        WHERE
            title LIKE %(title)s
            AND author LIKE %(author)s
        GROUP BY books.id
        {tag_search_clause}
        LIMIT 10
        OFFSET %(start)s
        """
        cursor.execute(query, payload)

        results = cursor.fetchall()

        if results is None:
            return []

        return [
            {
                "primaryText": title,
                "secondaryText": author,
                "chips": tags.strip().split(",") if tags is not None else [],
                "locator": (Destinations.bookInfo, id),
            }
            for id, title, author, tags in results
        ]

    @classmethod
    def searchCount(
        cls,
        title: str = "",
        author: str = "",
        tags: list[str] | None = None,
    ) -> int:
        """Searches books."""
        if tags is None:
            tags = []

        tag_search_clause = (
            (
                "HAVING "
                + "\n AND ".join(
                    f'IFNULL(GROUP_CONCAT(tags.name), "") LIKE "%{tag}%"'
                    for tag in tags
                )
            )
            if tags
            else ""
        )

        payload = {"title": f"%{title}%", "author": f"%{author}%"}

        query = f"""
        SELECT 1 FROM books
        LEFT JOIN book_tags ON
            books.id = book_tags.book_id
        LEFT JOIN tags ON
            book_tags.tag_id = tags.id
        WHERE
            title LIKE %(title)s
            AND author LIKE %(author)s
        GROUP BY books.id
        {tag_search_clause}
        """

        cursor.execute(query, payload)

        results = cursor.fetchall()

        if results is None:
            return 0

        return len(results)

    @classmethod
    def find_for_ui(cls, id: int, /):
        payload = {"id": id}

        cursor.execute(
            """
            SELECT
                books.title,
                books.author,
                books.cover_url,
                books.description,
                books.publisher,
                books.published_at,
                books.pages,
                COUNT(DISTINCT book_copies.id),
                GROUP_CONCAT(DISTINCT tags.name)
            FROM books
            JOIN book_copies ON
                book_copies.book_id = books.id
            JOIN book_tags ON
                book_tags.book_id = books.id
            JOIN tags ON
                book_tags.tag_id = tags.id
            GROUP BY books.id
            HAVING
                books.id = %(id)s
            """,
            payload,
        )

        result = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) FROM books
            JOIN book_copies ON
                book_copies.book_id = books.id
            JOIN loans ON
                loans.book_copy_id = book_copies.id
            WHERE
                loans.status = 'active'
            GROUP BY books.id
            HAVING
                books.id = %(id)s
            """,
            payload,
        )

        loaned_copies = cursor.fetchone()

        return (*result, loaned_copies[0] if loaned_copies is not None else 0)

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
            LIMIT 10
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
        publisher: str | None = None,
        published_at: date | None = None,
        pages: int | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Updates a book by its id."""
        book = cls.find_by_id(id)

        if tags is None:
            tags = []

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

        if publisher is not None:
            payload["publisher"] = publisher

        if published_at is not None:
            payload["published_at"] = published_at

        if pages is not None:
            payload["pages"] = pages

        cursor.execute(
            """
            UPDATE books
            SET
                title = %(title)s,
                author = %(author)s,
                cover_url = %(cover_url)s,
                description = %(description)s,
                publisher = %(publisher)s,
                published_at = %(published_at)s,
                pages = %(pages)s
            WHERE
                id = %(id)s
            """,
            payload,
        )

        payload = {"id": id}

        cursor.execute(
            """
            DELETE FROM book_tags
            WHERE
                book_id = %(id)s
            """,
            payload,
        )

        payload = [{"book_id": id, "tag": tag} for tag in tags]

        cursor.executemany(
            """
            INSERT INTO book_tags (book_id, tag_id)
            VALUES (%(book_id)s, (SELECT tags.id FROM tags WHERE tags.name = %(tag)s))
            """,
            payload,
        )

        connection.commit()

    @classmethod
    def delete(cls, id: int, /) -> None:
        """Deletes a book by its id."""
        payload = {"id": id}

        cursor.execute(
            """
            DELETE FROM books
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

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
                publisher VARCHAR(255) NOT NULL,
                published_at DATE NOT NULL,
                pages INT NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        payload = BOOKS

        cursor.executemany(
            """
            INSERT INTO books (
                id,
                title,
                author,
                cover_url,
                description,
                publisher,
                published_at,
                pages
            )
            VALUES (
                %(id)s,
                %(title)s,
                %(author)s,
                %(cover_url)s,
                %(description)s,
                %(publisher)s,
                %(published_at)s,
                %(pages)s
            )
            """,
            payload,
        )
