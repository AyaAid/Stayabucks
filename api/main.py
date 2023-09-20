from fastapi import FastAPI, APIRouter
from routes import login, sign_up

app = FastAPI()
router = APIRouter()

# Endpoint pour l'inscription


@router.post("/signup/")
async def signup(user: sign_up.UserCreate):
    """
    Endpoint pour l'inscription d'un nouvel utilisateur.

    Args:
        user (UserCreate): Informations de l'utilisateur à inscrire.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.
    """
    return sign_up.signup_user(user)

# Endpoint pour la connexion


@router.post("/login/")
async def login_endpoint(email: str, password: str):
    """
    Endpoint pour la connexion d'un utilisateur existant.

    Args:
        email (str): Mail de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de l'authentification.
    """
    return login.login_user(email, password)

# Ajoutez le routeur à l'application FastAPI
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
