from fastapi import FastAPI
from routers import products, users, basic_auth_user, jwt_auth_user, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()  # CONTEXTO
# Routers

app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)
app.include_router(users_db.router)
app.mount('/static', StaticFiles(directory="static"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

# Iniciar server con: uvicorn main:app --reload
# Documentacion: Swagger --> /docs | Redocly --> /redoc
