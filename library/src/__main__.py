import sys

import click
from src.cli.main import main


@main.command()
def run():
    # import json
    # from datetime import date as d

    # from src.models.book import Book
    # from src.models.tag import Tag

    # monthToNumber = {
    #     "January": 1,
    #     "February": 2,
    #     "March": 3,
    #     "April": 4,
    #     "May": 5,
    #     "June": 6,
    #     "July": 7,
    #     "August": 8,
    #     "September": 9,
    #     "October": 10,
    #     "November": 11,
    #     "December": 12,
    # }
    # with open(
    #     r"C:\Users\kaush\Google Drive\My Code\Library\library\library\src\data_getter\gottenData\tagsDataFinal.json",
    #     "r",
    # ) as f:
    #     tags = json.load(f)
    #     for tag in tags:
    #         Tag.create(tag["name"])
    # with open(
    #     r"C:\Users\kaush\Google Drive\My Code\Library\library\library\src\data_getter\gottenData\bookDataFinal.json",
    #     "r",
    # ) as f:
    #     books = json.load(f)
    #     from random import randint
    #     for book in books:
    #         date = book["published_at"].split("-")
    #         year = int(date[2])
    #         month = monthToNumber[date[1]]
    #         day = int(date[0])
    #         Book.create(
    #             author=book["author"],
    #             title=book["title"],
    #             cover_url=book["cover_url"],
    #             description=book["description"],
    #             publisher=book["publisher"],
    #             published_at=d(year, month, day),
    #             pages=book["pages"],
    #             copies=randint(1, 5),
    #             tags=book["tags"],
    #         )
    # import json
    # from src.models.user import User
    # with open(
    #     r"C:\Users\kaush\Google Drive\My Code\Library\library\library\src\data_getter\gottenData\peopleDataFinal.json",
    #     "r",
    # ) as f:
    #     people = json.load(f)
    #     for person in people:
    #         User.create(person["name"])

    # from src.models.loan import Loan
    # from src.models.book_copy import BookCopy
    # from src.database import cursor
    # from datetime import date, timedelta
    # cursor.execute("select id from book_copies;")
    # bcs = [i[0] for i in cursor.fetchall()]


    # from random import randint, choices

    # for person in range(1, 101):
    #     loanCount = randint(0, 7)
    #     for _ in range(loanCount):
    #         i = randint(0, len(bcs) - 1)
    #         bc = bcs.pop(i)
    #         createdDate = date(randint(2019, 2022), randint(1, 12), randint(1, 28))
    #         dueDate = createdDate + timedelta(days=7)
    #         xs = Loan.create(person, bc, createdDate, dueDate)

    #         if randint(1, 10) > 9:
    #             Loan.update(xs.id, status='overdue')       
    #         else:
    #             Loan.update(xs.id, status='returned', returned_at=dueDate-timedelta(days=randint(1, 6)))
    # for person in range(1, 101):
    #     loanCount = randint(0, 1)
    #     for _ in range(loanCount):
    #         i = randint(0, len(bcs) - 1)
    #         bc = bcs.pop(i)
    #         createdDate = date(2023, 1, randint(2, 12))
    #         dueDate = createdDate + timedelta(days=7)
    #         xs = Loan.create(person, bc, createdDate, dueDate)

    import src.ui
    pass


main()
