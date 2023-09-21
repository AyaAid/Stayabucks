from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from config.database import DatabaseConnection

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str
    email: str


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
            # Check if the user already exists
            query = "SELECT * FROM users WHERE email = %s"
            db_cursor.execute(query, (user.email,))
            existing_user = db_cursor.fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")

            # Add the user to the database
            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
            values = (user.username, user.email, user.password, "user")
            db_cursor.execute(query, values)
            db_connection.commit()

            return {"message": "Registration successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during registration")


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
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            db_cursor.execute(query, (user_data.email, user_data.password))
            user = db_cursor.fetchone()

            if user is None:
                raise HTTPException(status_code=401, detail="Incorrect email or password")

            return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during authentication")


@router.post("/logout/", tags=["Authentication"])
def logout_user():
    """
    Handle user logout by closing the database connection.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If logout fails.
    """
    try:
        with DatabaseConnection() as (db_connection, _):
            return {"message": "Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during logout")


@router.put("/update/{user_id}", tags=["Authentication"])
def update_user(user_id: int, user_update: UserUpdate):
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
            # Check if the user exists
            query = "SELECT * FROM users WHERE id = %s"
            db_cursor.execute(query, (user_id,))
            existing_user = db_cursor.fetchone()

            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")

            # Update user information
            query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
            values = (user_update.username, user_update.email, user_id)
            db_cursor.execute(query, values)
            db_connection.commit()

            return {"message": "Update successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during update")
