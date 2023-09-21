import json
from typing import Dict

from fastapi import HTTPException, APIRouter, Query
from pydantic import BaseModel

from config.database import connect_to_database, close_database_connection

router = APIRouter()


class Drinks(BaseModel):
    user_id: int
    drink_id: int
    supplement_id: Dict


@router.post('/create-drink', tags=["Drinks"])
async def createdrinks(drinks: Drinks):
    """
    Function to create drinks in database
    :param drinks: class w/ requirement of database to create drinks
    :return: str w/ message of success or type of error
    """
    try:
        conn, cursor = connect_to_database()
        supplement_id_json = json.dumps(drinks.supplement_id)
        cursor.execute(
            "INSERT INTO drink_created (user_id, drink_id, supplement_id) VALUES (%s, %s, %s)",
            (drinks.user_id, drinks.drink_id, supplement_id_json)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Boisson créée avec succès"}, 200
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=e)


@router.get('/show-drinks/{user_id}', tags=["Drinks"])
async def showdrinks(user_id):
    """
    Function to retrieve drinks created by a specific user
    :param user_id: user ID to filter drinks
    :return: List of drinks or an error message
    """
    try:
        user_id = int(user_id)
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM drink_created WHERE user_id = %s",
            (user_id,)
        )
        drinks = cursor.fetchall()
        close_database_connection()
        if not drinks:
            raise HTTPException(
                status_code=404, detail="Aucune boisson trouvée pour cet utilisateur")
        return {"drinks": drinks}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/")
async def search_drinks(query: str = Query(..., description="Recherchez une boisson par nom ou description")):
    db_connection, db_cursor = connect_to_database()

    try:
        # Utilisez une requête SQL pour rechercher des boissons par nom ou description
        search_query = f"%{query}%"
        query = "SELECT * FROM drink WHERE name LIKE %s OR description LIKE %s"
        db_cursor.execute(query, (search_query, search_query))
        drinks = db_cursor.fetchall()

        return drinks
    except Exception as e:
        raise e
    finally:
        close_database_connection()

