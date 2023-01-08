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
    #     r"C:\Users\nandhagk\Projects\library\library\src\data_stealer\stolenData\tagsDataFinal.json",
    #     "r",
    # ) as f:
    #     tags = json.load(f)
    #     for tag in tags:
    #         Tag.create(tag["name"])
    # with open(
    #     r"C:\Users\nandhagk\Projects\library\library\src\data_stealer\stolenData\bookDataFinal.json",
    #     "r",
    # ) as f:
    #     books = json.load(f)
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
    #             copies=2,
    #             tags=book["tags"],
    #         )

    import src.ui


main()
