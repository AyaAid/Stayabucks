from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, Field
from config.database import DatabaseConnection  # Import the new connection class

router = APIRouter()


class Drinks(BaseModel):
    name: str = Field(..., description="The name is required")
    description: str = Field(..., description="The description is required")
    price: float = Field(..., description="The price is required")


class Supplement(BaseModel):
    name: str = Field(..., description="The name is required")
    price: float = Field(..., description="The price is required")
    type_id: int = Field(..., description="The type id is required")


@router.post("/add-drink/", tags=["Admin - Drinks"])
async def add_drink(drinks: Drinks):
    """
    Add a new drink to the database.

    Args:
        drinks (Drinks): Information about the drink to be added.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If adding the drink fails.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute(
                "INSERT INTO drink (name, description, price) VALUES (%s, %s, %s)",
                (drinks.name, drinks.description, drinks.price)
            )
            conn.commit()
        return {"message": "Drink added successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-drink/{drink_id}/", tags=["Admin - Drinks"])
async def update_drink(drink_id: int, updated_drink: Drinks):
    """
    Update drink information in the database.

    Args:
        drink_id (int): ID of the drink to be updated.
        updated_drink (Drinks): Updated information for the drink.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If updating the drink fails or if the drink does not exist.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
            drink_result = cursor.fetchone()

            if drink_result is None:
                return {"message": "The drink does not exist"}, 404

            cursor.execute(
                "UPDATE drink SET name = %s, description = %s, price = %s WHERE id = %s",
                (updated_drink.name, updated_drink.description, updated_drink.price, drink_id)
            )
            conn.commit()
        return {"message": "Drink updated successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-drink/{drink_id}/", tags=["Admin - Drinks"])
async def delete_drink(drink_id: int):
    """
    Delete a drink from the database.

    Args:
        drink_id (int): ID of the drink to be deleted.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If deleting the drink fails or if the drink does not exist.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute("SELECT id FROM drink WHERE id = %s", (drink_id,))
            drink_result = cursor.fetchone()

            if drink_result is None:
                return {"message": "The drink does not exist"}, 404

            cursor.execute("DELETE FROM drink WHERE id = %s", (drink_id,))
            conn.commit()
        return {"message": "Drink deleted successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-supplement/", tags=["Admin - Supplement"])
async def add_supplement(supplement: Supplement):
    """
    Add a new supplement to the database.

    Args:
        supplement (Supplement): Information about the supplement to be added.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If adding the supplement fails or if the supplement type does not exist.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (supplement.type_id,))
            type_result = cursor.fetchone()

            if type_result is None:
                return {"message": "The type does not exist"}, 404

            cursor.execute(
                "INSERT INTO supplement (name, price, type_id) VALUES (%s, %s, %s)",
                (supplement.name, supplement.price, supplement.type_id)
            )
            conn.commit()
        return {"message": "Supplement added successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update-supplement/{supplement_id}/", tags=["Admin - Supplement"])
async def update_supplement(supplement_id: int, updated_supplement: Supplement):
    """
    Update supplement information in the database.

    Args:
        supplement_id (int): ID of the supplement to be updated.
        updated_supplement (Supplement): Updated information for the supplement.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If updating the supplement fails, if the supplement does not exist,
        or if the supplement type does not exist.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
            supplement_result = cursor.fetchone()

            if supplement_result is None:
                return {"message": "The supplement does not exist"}, 404

            cursor.execute("SELECT id FROM supplement_type WHERE id = %s", (updated_supplement.type_id,))
            type_result = cursor.fetchone()

            if type_result is None:
                return {"message": "The supplement type does not exist"}, 404

            cursor.execute(
                "UPDATE supplement SET name = %s, price = %s, type_id = %s WHERE id = %s",
                (updated_supplement.name, updated_supplement.price, updated_supplement.type_id, supplement_id)
            )
            conn.commit()
        return {"message": "Supplement updated successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-supplement/{supplement_id}/", tags=["Admin - Supplement"])
async def delete_supplement(supplement_id: int):
    """
    Delete a supplement from the database.

    Args:
        supplement_id (int): ID of the supplement to be deleted.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If deleting the supplement fails or if the supplement does not exist.
    """
    try:
        with DatabaseConnection() as (conn, cursor):
            cursor.execute("SELECT id FROM supplement WHERE id = %s", (supplement_id,))
            supplement_result = cursor.fetchone()

            if supplement_result is None:
                return {"message": "The supplement does not exist"}, 404

            cursor.execute("DELETE FROM supplement WHERE id = %s", (supplement_id,))
            conn.commit()
        return {"message": "Supplement deleted successfully"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
