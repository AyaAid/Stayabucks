from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from config.database import DatabaseConnection

router = APIRouter()


class LikeCreate(BaseModel):
    user_id: int
    drink_created_id: int


@router.post("/likes/")
def add_like(like_create: LikeCreate):
    """
    Add a new "like" for a drink created by a specific user.

    Args:
        like_create (LikeCreate): Information about the "like."

    Returns:
        dict: A success message.

    Raises:
        HTTPException:
            - 404: If the user or the created drink is not found.
            - 500: If an unexpected error occurs during the operation.
    """
    try:
        # Use a context manager to handle the database connection
        with DatabaseConnection() as (db_connection, db_cursor):

            # Check if the user exists (you can add more checks here)
            query = "SELECT * FROM users WHERE id = %s"
            db_cursor.execute(query, (like_create.user_id,))
            existing_user = db_cursor.fetchone()

            if not existing_user:
                raise HTTPException(
                    status_code=404, detail="User not found")

            # Check if the created drink exists (you can add more checks here)
            query = "SELECT * FROM drink_created WHERE id = %s"
            db_cursor.execute(query, (like_create.drink_created_id,))
            existing_drink_created = db_cursor.fetchone()

            if not existing_drink_created:
                raise HTTPException(
                    status_code=404, detail="Created drink not found")

            # Add the "like" to the drink_created_likes table
            query = "INSERT INTO drink_created_likes (user_id, drink_created_id) VALUES (%s, %s)"
            values = (like_create.user_id, like_create.drink_created_id)
            db_cursor.execute(query, values)
            db_connection.commit()

            return {"message": "Like added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
