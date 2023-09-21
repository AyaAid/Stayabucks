from fastapi import FastAPI, APIRouter
from routers.drinks import router as create_drinks_router
from routers.admin import router as admin_router
from routers.authentication import router as authentication_router
from routers.ratings import router_ratings as ratings_router

app = FastAPI()

app.include_router(create_drinks_router)
app.include_router(admin_router)
app.include_router(authentication_router)
app.include_router(ratings_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
