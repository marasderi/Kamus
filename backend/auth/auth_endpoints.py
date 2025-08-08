from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import hashlib
import base64
import hmac
import json

# Database setup
DATABASE_URL = "postgresql://kamus@localhost/kamus"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT-like token generation using standard libraries
SECRET_KEY = "your_secret_key_here"
TOKEN_EXPIRE_MINUTES = 30

# FastAPI app and router
app = FastAPI()
router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_token(data: dict, expires_delta: timedelta = timedelta(minutes=TOKEN_EXPIRE_MINUTES)) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire.isoformat()})
    payload_bytes = json.dumps(payload).encode()
    signature = hmac.new(SECRET_KEY.encode(), payload_bytes, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload_bytes + b"." + signature).decode()
    return token

# Signup endpoint
@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Signin endpoint
@router.post("/signin", response_model=Token)
def signin(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Include router in app
app.include_router(router)
