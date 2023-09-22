from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from config.database import DatabaseConnection

router = APIRouter()


class LikeCreate(BaseModel):
    user_id: int
    drink_created_id: int

class FavCreate(BaseModel):
    user_id: int
    drink_created_id: int


@router.post("/likes/", tags=["Ratings"])
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
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        # Raise a custom HTTP exception with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/fav/", tags=["Ratings"])
# def add_fav(fav_create: FavCreate):
#     """
#     Adds a favorite drink for a user.
#
#     Args:
#         fav_create (FavCreate): The data for creating a favorite drink for a user.
#
#     Returns:
#         dict: A dictionary containing a success message if the favorite is added successfully.
#
#     Raises:
#         HTTPException: If an error occurs while processing the request, such as user not found or created drink not found.
#     """
#     try:
#         # Use a context manager to handle the database connection
#         with DatabaseConnection() as (db_connection, db_cursor):
#
#             # Check if the user exists (you can add more checks here)
#             query = "SELECT * FROM users WHERE id = %s"
#             db_cursor.execute(query, (fav_create.user_id,))
#             existing_user = db_cursor.fetchone()
#
#             if not existing_user:
#                 raise HTTPException(
#                     status_code=404, detail="User not found")
#
#             # Check if the created drink exists (you can add more checks here)
#             query = "SELECT * FROM drink_created WHERE id = %s"
#             db_cursor.execute(query, (fav_create.drink_created_id,))
#             existing_drink_created = db_cursor.fetchone()
#
#             if not existing_drink_created:
#                 raise HTTPException(
#                     status_code=404, detail="Created drink not found")
#
#             # Add the "like" to the drink_created_likes table
#             query = "INSERT INTO favoris (user_id, drink_created_id) VALUES (%s, %s)"
#             values = (fav_create.user_id, fav_create.drink_created_id)
#             db_cursor.execute(query, values)
#             db_connection.commit()
#
#             return {"message": "Fav added successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.get('/show-fav/{user_id}', tags=["Ratings"])
# async def show_fav(user_id):
#     """
#     Retrieves the favorite drinks of a user.
#
#     Args:
#         user_id (int): The ID of the user whose favorite drinks need to be retrieved.
#
#     Returns:
#         tuple: A tuple containing a dictionary with the user's favorite drinks and HTTP status code.
#
#     Raises:
#         HTTPException: If an error occurs while processing the request, such as user not found or no favorites found.
#     """
#     try:
#         user_id = int(user_id)
#         # Use the new connection class with a context manager
#         with DatabaseConnection() as (conn, cursor):
#             # Check if the user exists (you can add more checks here)
#             query = "SELECT * FROM users WHERE id = %s"
#             cursor.execute(query, (user_id,))
#             existing_user = cursor.fetchone()
#
#             if not existing_user:
#                 raise HTTPException(
#                     status_code=404, detail="User not found")
#
#             cursor.execute(
#                 "SELECT user_id, drink_created_id FROM favoris WHERE user_id = %s",
#                 (user_id,)
#             )
#             favoris = cursor.fetchall()
#             if not favoris:
#                 raise HTTPException(
#                     status_code=404, detail="Not favoris found")
#         return {"favoris": favoris}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
