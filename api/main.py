from fastapi import FastAPI, APIRouter
from routers.drinks import router as create_drinks_router
from routers.admin import router as admin_router
from routers.login import router_login
from routers.sign_up import router_sign_up
from routers.logout import router_logout
from routers.update_user import router_update_user

app = FastAPI()

# Endpoint pour l'inscription
# @router.post("/signup/")
# async def signup(user: sign_up.UserCreate):
#     return sign_up.signup_user(user)
#
# # Endpoint pour la connexion
# @router.post("/login/")
# async def login_endpoint(username: str, password: str):
#     return login.login_user(username, password)
#
# Ajoutez le routeur à l'application FastAPI

app.include_router(create_drinks_router)
app.include_router(admin_router)
app.include_router(router_login)
app.include_router(router_sign_up)
app.include_router(router_logout)
app.include_router(router_update_user)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
