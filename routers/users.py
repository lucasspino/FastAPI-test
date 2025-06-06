from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()  # CONTEXTO

# Iniciar server con: uvicorn users:app --reload


class User(BaseModel):
    id: int
    user: str
    name: str
    surname: str


users_list = [
    User(id=1, user="lucasspino_", name="Lucas", surname="Pino"),
    User(id=2, user="tomi.ed", name="Tomas", surname="Ederson"),
    User(id=3, user="n-aleka", name="Noemi", surname="Aleka"),
    User(id=4, user="marielmolina95", name="Mariel", surname="Molina"),
    User(id=5, user="tefii_s", name="Stefani", surname="Sagreb")
]


@router.get("/usersjson")
async def usersjson():
    return [
        {"user": "lucasspino_", "name": "Lucas", "surname": "Pino"},
        {"user": "tomi.ed", "name": "Tomas", "surname": "Ederson"},
        {"user": "n-aleka", "name": "Noemi", "surname": "Aleka"},
        {"user": "marielmolina95", "name": "Mariel", "surname": "Molina"},
        {"user": "tefii_s", "name": "Stefani", "surname": "Sagreb"}
    ]


@router.get("/users")
async def users():
    return users_list


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {'error': 'El usuario no existe'}


# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query : userquerys/?key=value (/?id=1)
@router.get("/userquerys")
async def user(id: int):
    return search_user(id)

# Satatus code como segfundo parametro refiere a un codigo establecido


@router.post("/user", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        # manejamos errores (FastAPI sabe cual es y maneja el error // si es 404 muestra el detail)
        raise HTTPException(status_code=204, detail="El usuario ya existe")

    users_list.append(user)
    return user


@router.put("/user")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {'error': 'No se pudo actualizar el usuario'}
    return user


@router.delete('/user/{id}')
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se pudo eliminar el usuario"}
