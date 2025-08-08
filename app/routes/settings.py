from fastapi import APIRouter

router = APIRouter()

@router.put("/update_settings/{username}")
async def update_settings(username: str):
    return {"msg": f"Settings updated for {username}"}
