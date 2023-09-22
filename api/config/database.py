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
        try:
            self.db_connection = mysql.connector.connect(**db_config)
            self.db_cursor = self.db_connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error during database connection: {err}")
            self.db_connection = None
            self.db_cursor = None

    def user_exists(self, user_id):
        """
        Check if a user exists in the database.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        try:
            query = "SELECT COUNT(*) FROM users WHERE id = %s"
            self.db_cursor.execute(query, (user_id,))
            result = self.db_cursor.fetchone()

            if result and 'COUNT(*)' in result and result['COUNT(*)'] > 0:
                return True  # User exists
            else:
                return False  # User does not exist
        except mysql.connector.Error as err:
            print(f"Error checking user existence: {err}")
            return False

    def drink_exists(self, drink_id):
        """
        Check if a drink exists in the database.

        Args:
            drink_id (int): The ID of the drink.

        Returns:
            bool: True if the drink exists, False otherwise.
        """
        try:
            query = "SELECT COUNT(*) FROM drink WHERE id = %s"
            self.db_cursor.execute(query, (drink_id,))
            result = self.db_cursor.fetchone()

            if result and 'COUNT(*)' in result and result['COUNT(*)'] > 0:
                return True  # Drink exists
            else:
                return False  # Drink does not exist
        except mysql.connector.Error as err:
            print(f"Error checking drink existence: {err}")
            return False

    def __enter__(self):
        try:
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
        print("Database connection succeeded.")
    else:
        print("Database connection failed. Please check connection parameters.")
