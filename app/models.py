# app/models.py
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username: str
    email: str
    password: str
    # Autres champs du profil utilisateur

class StarbucksDrink(BaseModel):
    name: str
    ingredients: List[str]
    # Autres détails de la boisson
