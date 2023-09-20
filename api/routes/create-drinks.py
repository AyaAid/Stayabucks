import logging

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

logging.basicConfig(filename='debug.txt', level=logging.DEBUG)

router = APIRouter()

env = load_dotenv(".env.dist")  # Chargez les variables d'environnement depuis le fichier .env.dist
logging.debug(f"Chargement des variables d'environnement : {env}")

