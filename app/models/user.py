from sqlalchemy import Column, Integer, String, Date, Text
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bio = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    city = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    social_links = Column(Text, nullable=True)
