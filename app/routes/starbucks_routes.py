from fastapi import APIRouter
from app.models import StarbucksDrink
from fastapi import APIRouter
router = APIRouter()

# Route pour créer une boisson Starbucks
@router.post("/create/")
async def create_starbucks_drink(drink: StarbucksDrink):
    # Logique pour créer une boisson Starbucks dans la base de données
    # Retournez une réponse appropriée

# Route pour récupérer les détails d'une boisson Starbucks par son nom
@router.get("/{drink_name}/")
async def get_starbucks_drink_details(drink_name: str):
    # Logique pour récupérer les détails d'une boisson Starbucks par son nom
    # Retournez les détails de la boisson