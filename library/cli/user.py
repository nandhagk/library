from click import argument, group, option

from library.models.user import User


@group()
def user() -> None:
    """User management commands."""


@user.command()
@option("--name", required=True, help="Name of the user")
def create(name: str) -> None:
    """Creates a user."""
    user = User.create(name=name)
    print(user)


@user.command()
@argument("id", type=int)
def find(id: int) -> None:
    """Finds a user by their id."""
    user = User.find(id)

    if user is None:
        print("User not found!")
        return

    print(user)


@user.command()
@argument("id", type=int)
@option("--name", help="Name of the user")
def update(id: int, name: str | None) -> None:
    """Updates a user by their id."""
    user = User.update(id, name=name)

    if user is None:
        print("User not found!")
        return

    print(user)


@user.command()
@argument("id", type=int)
def delete(id: int) -> None:
    """Deletes a user by their id."""
    user = User.delete(id)

    if user is None:
        print("User not found!")
        return

    print(user)
