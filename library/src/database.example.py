import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
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
