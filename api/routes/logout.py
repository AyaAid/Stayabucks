from fastapi import HTTPException
from .database import close_database_connection

def logout_user():
    try:
        # Vous pouvez ajouter d'autres opérations de déconnexion ici si nécessaire
        close_database_connection()
        return {"message": "Déconnexion réussie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la déconnexion")
