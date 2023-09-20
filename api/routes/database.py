import mysql.connector
import os
from dotenv import load_dotenv

# Chargez les variables d'environnement depuis le fichier .env.dist
load_dotenv("api/.env")

# Configuration de la connexion à la base de données en utilisant les informations du fichier .env.dist
db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "port": os.getenv("POSTGRES_PORT"),
}

db_connection = None
db_cursor = None

def connect_to_database():
    global db_connection, db_cursor
    try:
        # Créez une connexion à la base de données
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor(dictionary=True)
        return db_connection, db_cursor
    except mysql.connector.Error as err:
        raise err

def close_database_connection():
    global db_connection, db_cursor
    if db_cursor:
        db_cursor.close()
    if db_connection:
        db_connection.close()