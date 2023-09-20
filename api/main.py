from fastapi import FastAPI, APIRouter
from routes import login, sign_up

app = FastAPI()
router = APIRouter()

# Endpoint pour l'inscription
@router.post("/signup/")
async def signup(user: sign_up.UserCreate):
    return sign_up.signup_user(user)

# Endpoint pour la connexion
@router.post("/login/")
async def login_endpoint(username: str, password: str):
    return login.login_user(username, password)

# Ajoutez le routeur à l'application FastAPI
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)