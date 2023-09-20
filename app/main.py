from fastapi import FastAPI
from api.routes import starbucks_routes
from api.routes import user_routes, order_routes

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
