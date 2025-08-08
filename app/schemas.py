from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    role_id: int

class PostCreate(BaseModel):
    user_id: int
    content: str
