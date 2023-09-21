from fastapi import FastAPI
from routers.drinks import router as drinks_router
from routers.admin import router as admin_router
from routers.authentication import router as authentication_router

app = FastAPI()

# Ajoutez le routeur à l'application FastAPI
app.include_router(admin_router)
app.include_router(authentication_router)
app.include_router(drinks_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
