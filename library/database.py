import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysqlpass#123",
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE DATABASE IF NOT EXISTS library
    """
)

cursor.execute(
    """
    USE library
    """
)

print(123)
