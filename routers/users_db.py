from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument, errors

router = APIRouter(prefix='/userdb', tags=["userdb"], responses={
    status.HTTP_404_NOT_FOUND: {'message': 'No encontrado'}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path


@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query : userquerys/?key=value (/?id=1)
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Satatus code como segfundo parametro refiere a un codigo establecido


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        # manejamos errores (FastAPI sabe cual es y maneja el error // si es 404 muestra el detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


# @router.put("/", response_model=User)
# async def user(user: User):

#     user_dict = dict(user)
#     del user_dict["id"]
#     try:
#         result = db_client.local.users.find_one_and_replace(
#             {"_id", ObjectId(user.id)}, user_dict)
#         if result is None:
#             raise HTTPException(
#                 status_code=404, detail="Usuario no encontrado")
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail="No se pudo actualizar el usuario")

#     return search_user("_id", ObjectId(user.id))
@router.put("/", response_model=User)
async def user(user: User):
    # ① Construye dict y quita la clave id
    user_dict = user.model_dump()          # igual que dict(user) pero más limpio
    user_dict.pop("id", None)              # no pasa nada si no existe

    # ② Valida el ObjectId
    try:
        oid = ObjectId(user.id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")

    # ③ Intenta reemplazar y devuelve el documento actualizado
    try:
        updated = db_client.users.find_one_and_replace(
            {"_id": oid},                   # filtro correcto
            user_dict,                      # documento de reemplazo
            return_document=ReturnDocument.AFTER,
            upsert=False                    # no crees uno nuevo si no existe
        )
        if updated is None:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
    except errors.PyMongoError as e:
        # Muestra el error real en la respuesta para depurar
        raise HTTPException(status_code=500, detail=f"Error MongoDB: {e}")

    return updated           # coincide con response_model=User


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se pudo eliminar el usuario"}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {'error': 'El usuario no existe'}
