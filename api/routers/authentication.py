import re
import bcrypt
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, EmailStr, Field
from config.database import DatabaseConnection

router = APIRouter()

class UserCreate(BaseModel):
    username: str = Field(..., description="The username is required")
    email: EmailStr = Field(..., description="The email address is required")
    password: str = Field(..., description="The password is required")

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    user_id: str = Field(..., description="The user id is required")
    username: str = Field(..., description="The username is required")
    email: EmailStr = Field(..., description="The email address is required")
    password: str = Field(..., description="The password is required")

def is_valid_email(email):
    # Check email format using a regular expression
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return False
    return True

@router.post("/signup/", tags=["Authentication"])
async def signup(user: UserCreate):
    """
    Register a new user in the database.

    Args:
        user (UserCreate): User information for registration.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If registration fails.
    """
    try:
        with DatabaseConnection() as (db_connection, db_cursor):
            if not is_valid_email(user.email):
                raise HTTPException(status_code=400, detail="Invalid email format")

            # Check if the user already exists
            query = "SELECT * FROM users WHERE email = %s"
            db_cursor.execute(query, (user.email,))
            existing_user = db_cursor.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")

            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

            # Add the user to the database
            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
            values = (user.username, user.email, hashed_password, "user")
            db_cursor.execute(query, values)
            db_connection.commit()

            return {"message": "Registration successful"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        # Raise a custom HTTP exception with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login/", tags=["Authentication"])
async def login_endpoint(user_data: UserLogin):
    """
    Verify user credentials in the database and perform login.

    Args:
        user_data (UserLogin): User login credentials (email and password).

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        with DatabaseConnection() as (db_connection, db_cursor):
            # Search for the user in the database
            query = "SELECT * FROM users WHERE email = %s"
            db_cursor.execute(query, (user_data.email,))
            user = db_cursor.fetchone()

            if user is None:
                raise HTTPException(status_code=401, detail="Incorrect email or password")

            # Vérifier le mot de passe haché avec bcrypt
            stored_password_hash = user["password"]
            provided_password = user_data.password.encode('utf-8')

            if bcrypt.checkpw(provided_password, stored_password_hash.encode('utf-8')):
                return {"message": "Login successful"}
            else:
                raise HTTPException(status_code=401, detail="Incorrect email or password")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        # Raise a custom HTTP exception with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/", tags=["Authentication"])
def update_user(user_update: UserUpdate):
    """
    Update user information in the database.

    Args:
        user_id (int): ID of the user to be updated.
        user_update (UserUpdate): Updated user information.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the update fails or if the user is not found.
    """
    try:
        with DatabaseConnection() as (db_connection, db_cursor):
            if not is_valid_email(user_update.email):
                raise HTTPException(status_code=400, detail="Invalid email format")

            # Check if the user exists
            query = "SELECT * FROM users WHERE id = %s"
            db_cursor.execute(query, (user_update.user_id,))
            existing_user = db_cursor.fetchone()

            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")

            # Update user information
            query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
            values = (user_update.username, user_update.email, user_update.user_id)
            db_cursor.execute(query, values)
            db_connection.commit()

            return {"message": "Update successful"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        # Raise a custom HTTP exception with a 500 status code
        raise HTTPException(status_code=500, detail=str(e))
