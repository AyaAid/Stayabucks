from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .database import connect_to_database, close_database_connection

router = APIRouter()


class Drinks(BaseModel):
    name: str
    description: str
    price: float


class Supplement(BaseModel):
    name: str
    price: float
    type_id: int


@router.post("/add-drink/")
async def add_drink(drinks: Drinks):
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO drink (name, description, price) VALUES (%s, %s, %s)",
            (drinks.name, drinks.description, drinks.price)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Boisson ajoutée avec succès"}  # Fixed the French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-supplement/")
async def add_supplement(supplement: Supplement):
    try:
        conn, cursor = connect_to_database()

        # Check if the type_id exists in the supplement_type table
        cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (supplement.type_id,))
        type_result = cursor.fetchone()

        if type_result is None:
            close_database_connection()
            return {"message": "Le type n'existe pas"}  # Type doesn't exist

        # Type exists, proceed to insert the supplement
        cursor.execute(
            "INSERT INTO supplement (name, price, type_id) VALUES (%s, %s, %s)",
            (supplement.name, supplement.price, supplement.type_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Supplément ajouté avec succès"}  # Fixed the French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-drink/{drink_id}/")
async def update_drink(drink_id: int, updated_drink: Drinks):
    try:
        conn, cursor = connect_to_database()

        # Check if the drink with the specified ID exists
        cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
        drink_result = cursor.fetchone()

        if drink_result is None:
            close_database_connection()
            return {"message": "La boisson n'existe pas"}  # Drink doesn't exist

        # Drink exists, proceed to update it
        cursor.execute(
            "UPDATE drink SET name = %s, description = %s, price = %s WHERE id = %s",
            (updated_drink.name, updated_drink.description, updated_drink.price, drink_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Boisson mise à jour avec succès"}  # Updated French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-supplement/{supplement_id}/")
async def update_supplement(supplement_id: int, updated_supplement: Supplement):
    try:
        conn, cursor = connect_to_database()

        # Check if the supplement with the specified ID exists
        cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
        supplement_result = cursor.fetchone()

        if supplement_result is None:
            close_database_connection()
            return {"message": "Le supplément n'existe pas"}  # Supplement doesn't exist

        # Check if the type_id exists in the supplement_type table
        cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (updated_supplement.type_id,))
        type_result = cursor.fetchone()

        if type_result is None:
            close_database_connection()
            return {"message": "Le type du supplément n'existe pas"}  # Type doesn't exist

        # Supplement and type exist, proceed to update
        cursor.execute(
            "UPDATE supplement SET name = %s, price = %s, type_id = %s WHERE id = %s",
            (updated_supplement.name, updated_supplement.price, updated_supplement.type_id, supplement_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Supplément mis à jour avec succès"}  # Updated French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/delete-drink/{drink_id}/")
async def delete_drink(drink_id: int):
    try:
        conn, cursor = connect_to_database()

        # Check if the drink with the specified ID exists
        cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
        drink_result = cursor.fetchone()

        if drink_result is None:
            close_database_connection()
            return {"message": "La boisson n'existe pas"}  # Drink doesn't exist

        # Drink exists, proceed to delete it
        cursor.execute("DELETE FROM drink WHERE id = %s", (drink_id,))
        conn.commit()
        close_database_connection()
        return {"message": "Boisson supprimée avec succès"}  # Updated French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-supplement/{supplement_id}/")
async def delete_supplement(supplement_id: int):
    try:
        conn, cursor = connect_to_database()

        # Check if the supplement with the specified ID exists
        cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
        supplement_result = cursor.fetchone()

        if supplement_result is None:
            close_database_connection()
            return {"message": "Le supplément n'existe pas"}  # Supplement doesn't exist

        # Supplement exists, proceed to delete it
        cursor.execute("DELETE FROM supplement WHERE id = %s", (supplement_id,))
        conn.commit()
        close_database_connection()
        return {"message": "Supplément supprimé avec succès"}  # Updated French message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
