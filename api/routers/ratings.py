from fastapi import HTTPException, APIRouter
from .database import connect_to_database, close_database_connection
from pydantic import BaseModel

router_ratings = APIRouter()


class LikeCreate(BaseModel):
    user_id: int
    # Utilisez le champ drink_created_id pour faire référence aux boissons créées par les utilisateurs.
    drink_created_id: int


@router_ratings.post("/likes/")
def add_like(like_create: LikeCreate):
    """
    Ajoute un nouveau "like" pour une boisson créée par un utilisateur donné.

    Args:
        like_create (LikeCreate): Informations sur le "like".

    Returns:
        Dict[str, str]: Un message de succès.
    """
    db_connection, db_cursor = connect_to_database()

    try:
        # Vérifiez si l'utilisateur existe (vous pouvez ajouter d'autres vérifications ici)
        query = "SELECT * FROM users WHERE id = %s"
        db_cursor.execute(query, (like_create.user_id,))
        existing_user = db_cursor.fetchone()

        if not existing_user:
            raise HTTPException(
                status_code=404, detail="Utilisateur non trouvé")

        # Vérifiez si la boisson créée existe (vous pouvez ajouter d'autres vérifications ici)
        query = "SELECT * FROM drink_created WHERE id = %s"
        db_cursor.execute(query, (like_create.drink_created_id,))
        existing_drink_created = db_cursor.fetchone()

        if not existing_drink_created:
            raise HTTPException(
                status_code=404, detail="Boisson créée non trouvée")

        # Ajoutez le "like" à la table drink_created_likes
        query = "INSERT INTO drink_created_likes (user_id, drink_created_id) VALUES (%s, %s)"
        values = (like_create.user_id, like_create.drink_created_id)
        db_cursor.execute(query, values)
        db_connection.commit()

        return {"message": "Like ajouté avec succès"}
    except Exception as e:
        raise e
    finally:
        close_database_connection()
