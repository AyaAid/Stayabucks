<<<<<<< HEAD
from fastapi import FastAPI, APIRouter
from routes import login, sign_up, logout, update_user
=======
from fastapi import FastAPI
from routes.login import router_login
from routes.sign_up import router_sign_up

>>>>>>> ec6318280137549dd45665f1870bb31ade36b972
app = FastAPI()

# Endpoint pour la déconnexion
@router.post("/logout/")
async def logout():
    """
    Endpoint pour la déconnexion de l'utilisateur.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.
    """
    return logout.logout_user()

# Endpoint pour la mise à jour des informations de l'utilisateur
@router.put("/update/{user_id}")
async def update_user_info(user_id: int, user_update: update_user.UserUpdate):
    """
    Endpoint pour la mise à jour des informations de l'utilisateur.

    Args:
        user_id (int): ID de l'utilisateur à mettre à jour.
        user_update (UserUpdate): Informations mises à jour de l'utilisateur.

    Returns:
        Dict[str, str]: Un dictionnaire contenant un message de succès.

    Raises:
        HTTPException: En cas d'échec de la mise à jour.
    """
    return update_user.update_user(user_id, user_update)

# Ajoutez le routeur à l'application FastAPI
app.include_router(router_login)
app.include_router(router_sign_up)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
