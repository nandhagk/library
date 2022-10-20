from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Final, cast

from library.database import connection, cursor

TAGS: Final = [
    {"id": 1, "name": "Action"},
    {"id": 2, "name": "Adventure"},
]


@dataclass(frozen=True)
class Tag:
    id: int
    name: str

    @staticmethod
    def create(name: str) -> Tag:
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
        tag = cast(Tag, Tag.find(id))

        return tag

    @staticmethod
    def find(id: int, /) -> Tag | None:
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

        return Tag(*result)

    @staticmethod
    def update(id: int, /, name: str | None = None) -> Tag | None:
        """Updates a tag by its id."""
        tag = Tag.find(id)

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

        return cast(Tag, Tag.find(id))

    @staticmethod
    def delete(id: int, /) -> Tag | None:
        """Deletes a tag by its id."""
        tag = Tag.find(id)

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

    @staticmethod
    def init() -> None:
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
                name VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        payload = TAGS

        cursor.executemany(
            """
            INSERT INTO tags (id, name)
            VALUES (%(id)s, %(name)s)
            """,
            payload,
        )

        connection.commit()
