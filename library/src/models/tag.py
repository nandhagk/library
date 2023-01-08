from dataclasses import asdict, dataclass
from typing import Final, cast

from src.database import connection, cursor
from typing_extensions import Self

TAGS: Final = [
    {"id": 1, "name": "Action"},
    {"id": 2, "name": "Adventure"},
    {"id": 3, "name": "Magazine"},
]


@dataclass(frozen=True)
class Tag:
    id: int
    name: str

    @classmethod
    def create(cls, name: str) -> Self:
        """Creates a tag."""
        payload = {"name": name}

        cursor.execute(
            """
            INSERT INTO tags (name)
            VALUES (%(name)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        tag = cast(cls, cls.find_by_id(id))

        return tag

    @classmethod
    def find_by_id(cls, id: int, /) -> Self | None:
        """Finds a tag by its id."""
        payload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM tags
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
    def exists(cls, name: int, /) -> Self | None:
        """Finds a tag by its name."""
        payload = {"name": name}

        cursor.execute(
            """
            SELECT * FROM tags
            WHERE
                name = %(name)s
            """,
            payload,
        )

        result = cursor.fetchone()
        
        if result is None:
            return False

        return True

    @classmethod
    def find_by_book_id(cls, book_id: int, /) -> list[Self]:
        """Finds the tags for a book by its id."""
        payload = {"book_id": book_id}

        cursor.execute(
            """
            SELECT tags.* from tags
            JOIN book_tags ON
                tags.id = book_tags.tag_id
            WHERE
                book_tags.book_id = %(book_id)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [cls(*result) for result in results]

    @classmethod
    def update(cls, id: int, /, name: str | None = None) -> Self | None:
        """Updates a tag by its id."""
        tag = cls.find_by_id(id)

        if tag is None:
            return

        payload = asdict(tag)

        if name is not None:
            payload["name"] = name

        cursor.execute(
            """
            UPDATE tags
            SET
                name = %(name)s
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return cast(cls, cls.find_by_id(id))

    @classmethod
    def delete(cls, id: int, /) -> Self | None:
        """Deletes a tag by its id."""
        tag = cls.find_by_id(id)

        if tag is None:
            return

        payload = {"id": tag.id}

        cursor.execute(
            """
            DELETE FROM tags
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return tag

    @classmethod
    def init(cls) -> None:
        """Initializes the tags table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS tags
            """
        )

        cursor.execute(
            """
            CREATE TABLE tags (
                id INT AUTO_INCREMENT,
                name VARCHAR(255) UNIQUE NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        # payload = TAGS

        # cursor.executemany(
        #     """
        #     INSERT INTO tags (id, name)
        #     VALUES (%(id)s, %(name)s)
        #     """,
        #     payload,
        # )

        # connection.commit()
