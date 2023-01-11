import json
from datetime import date, timedelta
from pathlib import Path
import json
from random import randint, choices
from datetime import date as d
from click import group
from src.database import cursor
from src.models.book import Book
from src.models.book_copy import BookCopy
from src.models.book_tag import BookTag
from src.models.loan import Loan
from src.models.tag import Tag
from src.models.user import User


@group()
def main() -> None:
    """Launches the app."""


@main.command()
def init() -> None:
    """Initializes the database."""
    cursor.execute(
        """
        DROP DATABASE IF EXISTS library
        """
    )

    cursor.execute(
        """
        CREATE DATABASE library
        """
    )

    cursor.execute(
        """
        USE library
        """
    )

    Tag.init()
    Book.init()
    User.init()
    BookTag.init()
    BookCopy.init()
    Loan.init()

    print("Successfully initialized the database!")
    

    monthToNumber = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    with open(
        Path(__file__).parent.parent.joinpath(r".\data_getter\gottenData\tagsDataFinal.json").as_posix(),
        "r",
    ) as f:
        tags = json.load(f)
        for tag in tags:
            Tag.create(tag["name"])
    with open(
         Path(__file__).parent.parent.joinpath(r".\data_getter\gottenData\bookDataFinal.json").as_posix(),
        "r",
    ) as f:
        books = json.load(f)
        
        for book in books:
            date = book["published_at"].split("-")
            year = int(date[2])
            month = monthToNumber[date[1]]
            day = int(date[0])
            Book.create(
                author=book["author"],
                title=book["title"],
                cover_url=book["cover_url"],
                description=book["description"],
                publisher=book["publisher"],
                published_at=d(year, month, day),
                pages=book["pages"],
                copies=randint(1, 5),
                tags=book["tags"],
            )
    with open(
        Path(__file__).parent.parent.joinpath(r".\data_getter\gottenData\peopleDataFinal.json").as_posix(),
        "r",
    ) as f:
        people = json.load(f)
        for person in people:
            User.create(person["name"])

    cursor.execute("select id from book_copies;")
    bcs = [i[0] for i in cursor.fetchall()]


    

    for person in range(1, 101):
        loanCount = randint(0, 7)
        for _ in range(loanCount):
            i = randint(0, len(bcs) - 1)
            bc = bcs.pop(i)
            createdDate = d(randint(2019, 2022), randint(1, 12), randint(1, 28))
            dueDate = createdDate + timedelta(days=7)
            xs = Loan.create(person, bc, createdDate, dueDate)

            if randint(1, 10) > 9:
                Loan.update(xs.id, status='overdue')       
            else:
                Loan.update(xs.id, status='returned', returned_at=dueDate-timedelta(days=randint(1, 6)))
    for person in range(1, 101):
        loanCount = randint(0, 1)
        for _ in range(loanCount):
            i = randint(0, len(bcs) - 1)
            bc = bcs.pop(i)
            createdDate = d(2023, 1, randint(2, 12))
            dueDate = createdDate + timedelta(days=7)
            xs = Loan.create(person, bc, createdDate, dueDate)
    print("Added the data :)")