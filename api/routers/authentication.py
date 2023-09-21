from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.database import connect_to_database, close_database_connection

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# Endpoint pour l'inscription
@router.post("/signup/", tags=["Authentication"])
async def signup(user: UserCreate):
    """
    Inscrit un nouvel utilisateur dans la base de données.

    Args:
        user (UserCreate): Informations de l'utilisateur à inscrire.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de l'inscription.
    """
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
        raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")
    finally:
        close_database_connection()


# Endpoint pour la connexion
@router.post("/login/", tags=["Authentication"])
async def login_endpoint(user_data: UserLogin):
    """
    Vérifie les informations d'identification de l'utilisateur dans la base de données et effectue la connexion.

    Args:
        user_data (UserLogin): Données d'identification de l'utilisateur (email et mot de passe).

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de l'authentification.
    """
    db_connection, db_cursor = connect_to_database()

    try:
        # Recherchez l'utilisateur dans la base de données
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        db_cursor.execute(query, (user_data.email, user_data.password))
        user = db_cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=401, detail="Mail de l'utilisateur ou mot de passe incorrect")

        return {"message": "Connexion réussie"}


    # TODO Faire l'exception 500
    finally:
        close_database_connection()
