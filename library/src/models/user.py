from dataclasses import asdict, dataclass
from typing import Final, cast

from src.database import connection, cursor
from src.pages import Destinations
from typing_extensions import Self

USERS: Final = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Doe"},
]


@dataclass(frozen=True)
class User:
    id: int
    name: str

    @classmethod
    def create(cls, name: str) -> Self:
        """Creates a user."""
        payload = {"name": name}

        cursor.execute(
            """
            INSERT INTO users (name)
            VALUES (%(name)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        user = cast(cls, cls.find_by_id(id))

        return user

    @classmethod
    def exists(cls, id: int, /) -> bool:
        return bool(cls.find_by_id(id))

    @classmethod
    def search(cls, name: str = "", start: int = 0) -> list[dict]:
        """Searches users."""
        payload = {"name": f"%{name}%", "start": start}

        cursor.execute(
            """
            SELECT id, name from users
            WHERE
                name LIKE %(name)s
            LIMIT 10
            OFFSET %(start)s
            """,
            payload,
        )

        results = cursor.fetchall()

        if results is None:
            return []

        return [
            {
                "primaryText": name,
                "secondaryText": "",
                "chips": [],
                "locator": (Destinations.personInfo, id),
            }
            for id, name in results
        ]

    @classmethod
    def searchCount(cls, name: str = "") -> int:
        """Searches users."""
        payload = {"name": f"%{name}%"}

        cursor.execute(
            """
            SELECT COUNT(*) from users
            WHERE
                name LIKE %(name)s
            """,
            payload,
        )

        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    @classmethod
    def find_by_id(cls, id: int, /) -> Self | None:
        """Finds a user by their id."""
        payload = {"id": id}

        cursor.execute(
            """
            SELECT * FROM users
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
    def update(cls, id: int, /, name: str | None = None) -> Self | None:
        """Updates a user by their id."""
        user = cls.find_by_id(id)

        if user is None:
            return

        payload = asdict(user)

        if name is not None:
            payload["name"] = name

        cursor.execute(
            """
            UPDATE users
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
        """Deletes a user by their id."""
        user = cls.find_by_id(id)

        if user is None:
            return

        payload = {"id": user.id}

        cursor.execute(
            """
            DELETE FROM users
            WHERE
                id = %(id)s
            """,
            payload,
        )

        connection.commit()

        return user

    @classmethod
    def init(cls) -> None:
        """Initializes the users table."""
        cursor.execute(
            """
            DROP TABLE IF EXISTS users
            """
        )

        cursor.execute(
            """
            CREATE TABLE users (
                id INT AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        # payload = USERS

        # cursor.executemany(
        #     """
        #     INSERT INTO users (id, name)
        #     VALUES (%(id)s, %(name)s)
        #     """,
        #     payload,
        # )

        # connection.commit()
