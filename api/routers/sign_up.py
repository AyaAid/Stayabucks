from fastapi import HTTPException, APIRouter
from .database import connect_to_database, close_database_connection
from pydantic import BaseModel

router_sign_up = APIRouter()

# Modèle Pydantic pour la création d'un nouvel utilisateur


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router_sign_up.post("/signup/")
def signup_user(user: UserCreate):
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
        raise e
    finally:
        close_database_connection()
