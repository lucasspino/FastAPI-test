from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None  # Dar un valor por defecto si o si
    username: str
    email: str
