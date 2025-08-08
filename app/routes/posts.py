from fastapi import APIRouter
from app.schemas import PostCreate

router = APIRouter()

@router.post("/")
def create_post(post: PostCreate):
    return {"message": "Post created", "post": post}
