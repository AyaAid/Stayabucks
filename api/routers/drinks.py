import json
from typing import Dict

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from config.database import close_database_connection, connect_to_database

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
    Retrieves drinks created by a specific user.
    Args:
        user_id (int): The ID of the user whose drinks are to be retrieved.
    Returns:
        dict: A dictionary containing the drinks and their total prices.
    """
    try:
        user_id = int(user_id)
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT drink_id, supplement_id FROM drink_created WHERE user_id = %s",
            (user_id,)
        )
        drinks = cursor.fetchall()
        drinks_with_prices = []
        for drink_data in drinks:
            supplement_id_list = json.loads(drink_data['supplement_id']) if drink_data['supplement_id'] else {}
            cursor.execute("SELECT price FROM drink WHERE id = %s", (drink_data['drink_id'],))
            drink_price = cursor.fetchone()
            if drink_price:
                drink_price = drink_price['price']
                total_price = drink_price
                for supplement_id, quantity in supplement_id_list.items():
                    cursor.execute("SELECT price FROM supplement WHERE id = %s", (supplement_id,))
                    supplement_price = cursor.fetchone()
                    if supplement_price:
                        supplement_price = supplement_price['price']
                        total_price += supplement_price * quantity
                drinks_with_prices.append({
                    "drink_id": drink_data['drink_id'],
                    "total_price": total_price
                })

        close_database_connection()
        if not drinks_with_prices:
            raise HTTPException(status_code=404, detail="Aucune boisson trouvée pour cet utilisateur")

        return {"drinks": drinks_with_prices}, 200
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplement_ids data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/last-drinks/{user_id}', tags=["Drinks"])
async def lastdrinks(user_id):
    """
    Retrieve the 10 most recent drinks created by a specific user.

    Args:
        user_id (int): The ID of the user whose drinks are to be retrieved.

    Returns:
        dict: A dictionary containing the list of drinks or an error message.

    Raises:
        HTTPException:
            - 404: If no drinks are found for the specified user.
            - 500: If an unexpected error occurs during the operation.

    Example:
        To retrieve the 10 most recent drinks for user with ID 123:
        GET /last-drinks/123
    """
    try:
        user_id = int(user_id)
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM drink_created WHERE user_id = %s ORDER BY id DESC LIMIT 10",
            (user_id,)
        )
        drinks = cursor.fetchall()
        close_database_connection()
        if not drinks:
            raise HTTPException(status_code=404, detail="Aucune boisson trouvée pour cet utilisateur")
        return {"drinks": drinks}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

