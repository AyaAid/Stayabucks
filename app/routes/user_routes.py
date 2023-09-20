from fastapi import APIRouter, Depends
from app.models import User
from app.auth import get_current_user

router = APIRouter()

@router.post("/signup/")
async def signup(user: User):
    # Logique pour créer un nouvel utilisateur dans la base de données
    # Assurez-vous de hacher le mot de passe avant de le stocker
    # Retournez une réponse appropriée

@router.get("/profile/")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    # Logique pour obtenir le profil de l'utilisateur actuellement connecté
    # Retournez les détails du profil
