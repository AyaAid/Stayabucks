import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

# Configuration de la journalisation
logging.basicConfig(filename='debug.txt', level=logging.DEBUG)

router = APIRouter()

# Modèle Pydantic pour la création d'un nouvel utilisateur
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Configuration de la connexion à la base de données en utilisant les informations du fichier .env.dist
env = load_dotenv(".env.dist")  # Chargez les variables d'environnement depuis le fichier .env.dist
logging.debug(f"Chargement des variables d'environnement : {env}")

db_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "port": os.getenv("POSTGRES_PORT"),
}

db_connection = None
db_cursor = None

try:
    # Créez une connexion à la base de données
    logging.debug("Tentative de connexion à la base de données...")
    db_connection = mysql.connector.connect(**db_config)
    db_cursor = db_connection.cursor(dictionary=True)
    logging.debug("Connexion à la base de données réussie.")
except mysql.connector.Error as err:
    logging.error(f"Erreur de connexion à la base de données : {err}")

# Fonction pour s'inscrire (signup)
def signup_user(user: UserCreate):
    try:
        # Vérifiez si l'utilisateur existe déjà
        query = "SELECT * FROM users WHERE email = %s"
        db_cursor.execute(query, (user.email,))
        existing_user = db_cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")

        # Ajoutez l'utilisateur à la base de données
        query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        values = (user.username, user.email, user.password, "user")
        db_cursor.execute(query, values)
        db_connection.commit()

        return {"message": "Inscription réussie"}
    except Exception as e:
        logging.error(f"Erreur lors de l'inscription : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")

# Fonction pour se connecter (login)
def login_user(username: str, password: str):
    try:
        # Recherchez l'utilisateur dans la base de données
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        db_cursor.execute(query, (username, password))
        user = db_cursor.fetchone()

        if user:
            return {"message": "Connexion réussie"}

        # Si l'utilisateur n'est pas trouvé, renvoyez une erreur
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    except Exception as e:
        logging.error(f"Erreur lors de la connexion : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la connexion")

@router.post("/signup/")
async def signup_endpoint(user: UserCreate):
    return signup_user(user)

@router.post("/login/")
async def login_endpoint(username: str, password: str):
    return login_user(username, password)

if __name__ == "__main__":
    import uvicorn
    logging.debug("Démarrage de l'application FastAPI...")
    uvicorn.run(router, host="0.0.0.0", port=8000)
