from click import group

from library.cli.db.main import db


@group()
def main() -> None:
    """Launches the app."""


main.add_command(db)
