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


class UserUpdate(BaseModel):
    username: str
    email: str

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

@router.post("/logout/", tags=["Authentication"])
def logout_user():
    """
    Gère la déconnexion de l'utilisateur en fermant la connexion à la base de données.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de la déconnexion.
    """
    try:
        close_database_connection()
        return {"message": "Déconnexion réussie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la déconnexion")

@router.put("/update/{user_id}", tags=["Authentication"])
def update_user(user_id: int, user_update: UserUpdate):
    """
    Met à jour les informations de l'utilisateur dans la base de données.

    Args:
        user_id (int): ID de l'utilisateur à mettre à jour.
        user_update (UserUpdate): Informations mises à jour de l'utilisateur.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de la mise à jour ou si l'utilisateur n'est pas trouvé.
    """
    db_connection, db_cursor = connect_to_database()

    try:
        # Vérifiez si l'utilisateur existe
        query = "SELECT * FROM users WHERE id = %s"
        db_cursor.execute(query, (user_id,))
        existing_user = db_cursor.fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        # Mettez à jour les informations de l'utilisateur
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        values = (user_update.username, user_update.email, user_id)
        db_cursor.execute(query, values)
        db_connection.commit()

        return {"message": "Mise à jour réussie"}
    except Exception as e:
        raise e
    finally:
        close_database_connection()