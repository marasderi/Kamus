from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

class Role(BaseModel):
    id: int
    name: str

class Post(BaseModel):
    id: int
    user_id: int
    content: str
