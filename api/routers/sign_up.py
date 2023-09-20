from fastapi import HTTPException
from .database import connect_to_database, close_database_connection
from pydantic import BaseModel


# Modèle Pydantic pour la création d'un nouvel utilisateur
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


def signup_user(user: UserCreate):
    db_connection, db_cursor = connect_to_database()

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
        raise e
    finally:
        close_database_connection()