from fastapi import FastAPI
from routes.login import router_login
from routes.sign_up import router_sign_up
from routes.logout import router_logout
from routes.update_user import router_update_user

app = FastAPI()

# Ajoutez le routeur à l'application FastAPI
app.include_router(router_login)
app.include_router(router_sign_up)
app.include_router(router_logout)
app.include_router(router_update_user)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Fichier principal de l'application FastAPI Stayabucks.

Ce fichier configure l'application FastAPI en ajoutant des routeurs pour les fonctionnalités de connexion,
d'inscription, de déconnexion et de mise à jour de l'utilisateur.

"""
