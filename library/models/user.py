from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TypedDict, cast

from library.database import connection, cursor


class CreateUserPayload(TypedDict):
    name: str


class FindUserPayload(TypedDict):
    id: int


class UpdateUserPayload(TypedDict):
    id: int
    name: str


class DeleteUserPayload(TypedDict):
    id: int


@dataclass(frozen=True)
class User:
    id: int
    name: str

    @staticmethod
    def create(name: str) -> User:
        """Creates a user."""
        payload: CreateUserPayload = {"name": name}

        cursor.execute(
            """
            INSERT INTO users (name)
            VALUES (%(name)s)
            """,
            payload,
        )

        connection.commit()

        id = cast(int, cursor.lastrowid)
        user = cast(User, User.find(id))

        return user

    @staticmethod
    def find(id: int, /) -> User | None:
        """Finds a user by their id."""
        payload: FindUserPayload = {"id": id}

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

        return User(*result)

    @staticmethod
    def update(id: int, /, name: str | None = None) -> User | None:
        """Updates a user by their id."""
        user = User.find(id)

        if user is None:
            return

        payload = cast(UpdateUserPayload, asdict(user))

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

        return cast(User, User.find(id))

    @staticmethod
    def delete(id: int, /) -> User | None:
        """Deletes a user by their id."""
        user = User.find(id)

        if user is None:
            return

        payload: DeleteUserPayload = {"id": user.id}

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

    @staticmethod
    def init() -> None:
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

        payload = [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Doe"},
        ]

        cursor.executemany(
            """
            INSERT INTO users (id, name)
            VALUES (%(id)s, %(name)s)
            """,
            payload,
        )

        connection.commit()
