import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(".env")

# Configuration for connecting to the MySQL database using information from the .env file
db_config = {
    "user": os.getenv("MYSQL_USER"),  # MySQL username
    "password": os.getenv("MYSQL_PASSWORD"),  # MySQL password
    "host": os.getenv("MYSQL_HOST"),  # MySQL host (e.g., "localhost")
    "database": os.getenv("MYSQL_DB"),  # MySQL database name
    "port": os.getenv("MYSQL_PORT"),  # MySQL port number
}


class DatabaseConnection:
    """
    A context manager for managing MySQL database connections.

    Usage:
        with DatabaseConnection() as (connection, cursor):
            # Database operations here

    Attributes:
        db_connection (mysql.connector.MySQLConnection): The database connection.
        db_cursor (mysql.connector.cursor.MySQLCursor): The database cursor.
    """

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def __enter__(self):
        try:
            # Create a connection to the MySQL database
            self.db_connection = mysql.connector.connect(**db_config)
            self.db_cursor = self.db_connection.cursor(dictionary=True)
            return self.db_connection, self.db_cursor
        except mysql.connector.Error as err:
            raise err

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db_cursor:
            self.db_cursor.close()
        if self.db_connection:
            self.db_connection.close()


# Using the MySQL database connection with a context manager
with DatabaseConnection() as (connection, cursor):
    if connection is not None and cursor is not None:
        # Database connection succeeded
        print("Database connection succeeded.")
    else:
        # Database connection failed, take appropriate action
        print("Database connection failed. Please check connection parameters.")
