from click import group, option

from library.src.models.tag import Tag


@group()
def tag() -> None:
    """Tag management commands."""


@tag.command()
@option("--name", required=True, help="Name of the tag")
def create(name: str) -> None:
    """Creates a tag."""
    tag = Tag.create(name=name)
    print(tag)


@tag.command()
@option("--id", type=int, required=True, help="ID of the tag")
def find(id: int) -> None:
    """Finds a tag by its id."""
    tag = Tag.find(id)

    if tag is None:
        print("Tag not found!")
        return

    print(tag)


@tag.command()
@option("--id", type=int, required=True, help="ID of the tag")
@option("--name", help="Name of the tag")
def update(id: int, name: str | None) -> None:
    """Updates a tag by its id."""
    tag = Tag.update(id, name=name)

    if tag is None:
        print("Tag not found!")
        return

    print(tag)


@tag.command()
@option("--id", type=int, required=True, help="ID of the tag")
def delete(id: int) -> None:
    """Deletes a tag by their id."""
    tag = Tag.delete(id)

    if tag is None:
        print("Tag not found!")
        return

    print(tag)
