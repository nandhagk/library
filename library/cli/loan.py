from click import group


@group()
def loan() -> None:
    """Loan management commands."""
