from fastapi import FastAPI
from app.models import User, StarbucksDrink
from app.auth import get_current_user
from app.routes import user_routes, starbucks_routes, order_routes

app = FastAPI()

# Inclure les routes d'utilisateur
app.include_router(user_routes.router, prefix="/user", tags=["user"])

# Inclure les routes Starbucks
app.include_router(starbucks_routes.router,
                   prefix="/starbucks", tags=["starbucks"])

# Inclure les routes de commande
app.include_router(order_routes.router, prefix="/order", tags=["order"])

# Reste du code pour les autres routes principales
# ...
