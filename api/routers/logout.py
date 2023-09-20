from fastapi import HTTPException, APIRouter
from .database import close_database_connection

router_logout = APIRouter()

@router_logout.post("/logout/")
def logout_user():
    """
    Gère la déconnexion de l'utilisateur en fermant la connexion à la base de données.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de la déconnexion.
    """
    try:
        close_database_connection()
        return {"message": "Déconnexion réussie"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la déconnexion")
