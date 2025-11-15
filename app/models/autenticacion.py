from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    id_rol: int
    