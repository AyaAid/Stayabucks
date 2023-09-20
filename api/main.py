from fastapi import FastAPI
from routes.login import router_login
from routes.sign_up import router_sign_up

app = FastAPI()

# Ajoutez le routeur à l'application FastAPI
app.include_router(router_login)
app.include_router(router_sign_up)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
