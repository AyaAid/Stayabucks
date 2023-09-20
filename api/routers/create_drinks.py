import json
from typing import Dict

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from .database import connect_to_database, close_database_connection

router = APIRouter()

class Drinks(BaseModel):
    user_id: int
    drink_id: int
    supplement_id: Dict


@router.post('/create-drink')
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
        return {"message": "Boisson créée avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=e)

