from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .database import connect_to_database, close_database_connection

router = APIRouter()


class Drinks(BaseModel):
    """Model for defining the structure of a drink."""
    name: str
    description: str
    price: float


class Supplement(BaseModel):
    """Model for defining the structure of a supplement."""
    name: str
    price: float
    type_id: int


@router.post("/add-drink/")
async def add_drink(drinks: Drinks):
    """
    Add a new drink to the database.

    Args:
        drinks (Drinks): The drink data to be added.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO drink (name, description, price) VALUES (%s, %s, %s)",
            (drinks.name, drinks.description, drinks.price)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Boisson ajoutée avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-supplement/")
async def add_supplement(supplement: Supplement):
    """
    Add a new supplement to the database.

    Args:
        supplement (Supplement): The supplement data to be added.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()

        cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (supplement.type_id,))
        type_result = cursor.fetchone()

        if type_result is None:
            close_database_connection()
            return {"message": "Le type n'existe pas"}, 404

        cursor.execute(
            "INSERT INTO supplement (name, price, type_id) VALUES (%s, %s, %s)",
            (supplement.name, supplement.price, supplement.type_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Supplément ajouté avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-drink/{drink_id}/")
async def update_drink(drink_id: int, updated_drink: Drinks):
    """
    Update an existing drink in the database.

    Args:
        drink_id (int): The ID of the drink to be updated.
        updated_drink (Drinks): The updated drink data.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()

        cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
        drink_result = cursor.fetchone()

        if drink_result is None:
            close_database_connection()
            return {"message": "La boisson n'existe pas"}, 404

        cursor.execute(
            "UPDATE drink SET name = %s, description = %s, price = %s WHERE id = %s",
            (updated_drink.name, updated_drink.description, updated_drink.price, drink_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Boisson mise à jour avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-supplement/{supplement_id}/")
async def update_supplement(supplement_id: int, updated_supplement: Supplement):
    """
    Update an existing supplement in the database.

    Args:
        supplement_id (int): The ID of the supplement to be updated.
        updated_supplement (Supplement): The updated supplement data.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()

        cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
        supplement_result = cursor.fetchone()

        if supplement_result is None:
            close_database_connection()
            return {"message": "Le supplément n'existe pas"}, 404

        cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (updated_supplement.type_id,))
        type_result = cursor.fetchone()

        if type_result is None:
            close_database_connection()
            return {"message": "Le type du supplément n'existe pas"}, 404

        cursor.execute(
            "UPDATE supplement SET name = %s, price = %s, type_id = %s WHERE id = %s",
            (updated_supplement.name, updated_supplement.price, updated_supplement.type_id, supplement_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Supplément mis à jour avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-drink/{drink_id}/")
async def delete_drink(drink_id: int):
    """
    Delete an existing drink from the database.

    Args:
        drink_id (int): The ID of the drink to be deleted.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()

        cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
        drink_result = cursor.fetchone()

        if drink_result is None:
            close_database_connection()
            return {"message": "La boisson n'existe pas"}, 404

        cursor.execute("DELETE FROM drink WHERE id = %s", (drink_id,))
        conn.commit()
        close_database_connection()
        return {"message": "Boisson supprimée avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-supplement/{supplement_id}/")
async def delete_supplement(supplement_id: int):
    """
    Delete an existing supplement from the database.

    Args:
        supplement_id (int): The ID of the supplement to be deleted.

    Returns:
        dict: A message indicating the success of the operation.
    """
    try:
        conn, cursor = connect_to_database()

        cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
        supplement_result = cursor.fetchone()

        if supplement_result is None:
            close_database_connection()
            return {"message": "Le supplément n'existe pas"}, 404

        cursor.execute("DELETE FROM supplement WHERE id = %s", (supplement_id,))
        conn.commit()
        close_database_connection()
        return {"message": "Supplément supprimé avec succès"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
