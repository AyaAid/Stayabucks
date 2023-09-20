from fastapi import HTTPException, APIRouter
from .database import connect_to_database, close_database_connection
from pydantic import BaseModel

router_update_user = APIRouter()

# Modèle Pydantic pour la mise à jour des informations de l'utilisateur
class UserUpdate(BaseModel):
    username: str
    email: str

@router_update_user.put("/update/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    """
    Met à jour les informations de l'utilisateur dans la base de données.

    Args:
        user_id (int): ID de l'utilisateur à mettre à jour.
        user_update (UserUpdate): Informations mises à jour de l'utilisateur.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de la mise à jour.
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
