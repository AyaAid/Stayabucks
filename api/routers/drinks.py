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
        return {"message": "Boisson créée avec succès"}, 200
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=e)


@router.get('/show-drinks/{user_id}')
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
        drinks_with_prices = []
        for drink_data in drinks:
            drink_id, supplement_ids = drink_data
            supplement_id_list = json.loads(supplement_ids)

            # Récupérer le prix de la boisson
            cursor.execute("SELECT price FROM drink WHERE id = %s", (drink_id,))
            drink_price = cursor.fetchone()[0]  # Supposant que la colonne price existe dans la table drinks

            # Calculer le prix total de la boisson en tenant compte des suppléments
            total_price = drink_price
            for supplement_id, quantity in supplement_id_list.items():
                # Récupérer le prix du supplément
                cursor.execute("SELECT price FROM supplement WHERE id = %s", (supplement_id,))
                supplement_price = cursor.fetchone()[
                    0]  # Supposant que la colonne price existe dans la table supplements
                total_price += supplement_price * quantity

            # Ajouter la boisson avec son prix total à la liste
            drinks_with_prices.append({
                "drink_id": drink_id,
                "total_price": total_price
            })
        close_database_connection()
        if not drinks:
            raise HTTPException(status_code=404, detail="Aucune boisson trouvée pour cet utilisateur")
        return {"drinks": drinks_with_prices}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))