from fastapi import FastAPI
from app.routes import users, posts

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(posts.router, prefix="/posts")

@app.get("/")
def read_root():
    return {"message": "Welcome to Kamus API"}
