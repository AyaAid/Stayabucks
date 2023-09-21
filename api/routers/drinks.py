import json
from typing import Dict

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from config.database import DatabaseConnection  # Import the new connection class

router = APIRouter()


class Drinks(BaseModel):
    user_id: int
    drink_id: int
    supplement_id: Dict


@router.post('/create-drink', tags=["Drinks"])
async def create_drink(drinks: Drinks):
    """
    Create drinks in the database.

    Args:
        drinks (Drinks): Information required to create drinks in the database.

    Returns:
        dict: A dictionary with a success message or an error type.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    try:
        # Use the new connection class with a context manager
        with DatabaseConnection() as (conn, cursor):
            supplement_id_json = json.dumps(drinks.supplement_id)
            cursor.execute(
                "INSERT INTO drink_created (user_id, drink_id, supplement_id) VALUES (%s, %s, %s)",
                (drinks.user_id, drinks.drink_id, supplement_id_json)
            )
            conn.commit()
        return {"message": "Drink created successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/show-drinks/{user_id}', tags=["Drinks"])
async def show_drinks(user_id):
    """
    Retrieve drinks created by a specific user.

    Args:
        user_id (int): The ID of the user whose drinks are to be retrieved.

    Returns:
        dict: A dictionary containing the drinks and their total prices.

    Raises:
        HTTPException:
            - 404: If no drinks are found for this user.
            - 400: If the supplement_ids data is invalid.
            - 500: If an unexpected error occurs during the operation.
    """
    try:
        user_id = int(user_id)
        # Use the new connection class with a context manager
        with DatabaseConnection() as (conn, cursor):
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

        if not drinks_with_prices:
            raise HTTPException(status_code=404, detail="No drinks found for this user")

        return {"drinks": drinks_with_prices}, 200
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplement_ids data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/last-drinks/{user_id}', tags=["Drinks"])
async def last_drinks(user_id):
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
    """
    try:
        user_id = int(user_id)
        # Use the new connection class with a context manager
        with DatabaseConnection() as (conn, cursor):
            cursor.execute(
                "SELECT * FROM drink_created WHERE user_id = %s ORDER BY id DESC LIMIT 10",
                (user_id,)
            )
            drinks = cursor.fetchall()

        if not drinks:
            raise HTTPException(status_code=404, detail="No drinks found for this user")
        return {"drinks": drinks}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
