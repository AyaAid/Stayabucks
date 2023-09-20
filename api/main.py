from fastapi import FastAPI
from routers.drinks import router as create_drinks_router
from routers.admin import router as admin_router
from routers.login import router_login
from routers.sign_up import router_sign_up
from routers.logout import router_logout
from routers.update_user import router_update_user
from routers.ratings import router_ratings

app = FastAPI()

app.include_router(create_drinks_router)
app.include_router(admin_router)
app.include_router(router_login)
app.include_router(router_sign_up)
app.include_router(router_logout)
app.include_router(router_update_user)
app.include_router(router_ratings)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
