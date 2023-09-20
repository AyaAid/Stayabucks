from fastapi import HTTPException
from .database import connect_to_database, close_database_connection

def login_user(email: str, password: str):
    db_cursor = connect_to_database()
    
    try:
        # Recherchez l'utilisateur dans la base de données
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        db_cursor.execute(query, (email, password))
        user = db_cursor.fetchone()

        if user:
            return {"message": "Connexion réussie"}

        # Si l'utilisateur n'est pas trouvé, renvoyez une erreur
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    except Exception as e:
        raise e
    finally:
        close_database_connection()