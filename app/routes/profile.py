from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserUpdate
from app.database import SessionLocal
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.put("/update_profile/{username}")
async def update_profile(username: str, updates: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    return {"msg": "Profile updated"}
