from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

# Simulated database
fake_user_db = {
    "john_doe": {
        "username": "john_doe",
        "email": "john@example.com",
        "birthdate": "1990-01-01",
        "gender": "male",
        "city": "Ankara",
        "profession": "Engineer",
        "interests": "Technology, Music",
        "social_links": {
            "twitter": "https://twitter.com/john_doe",
            "linkedin": "https://linkedin.com/in/johndoe"
        },
        "bio": "Hello, I'm John!"
    }
}

class SocialLinks(BaseModel):
    twitter: Optional[str]
    linkedin: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]

class ProfileUpdate(BaseModel):
    username: str
    email: Optional[str]
    birthdate: Optional[date]
    gender: Optional[str]
    city: Optional[str]
    profession: Optional[str]
    interests: Optional[str]
    social_links: Optional[SocialLinks]
    bio: Optional[str]

@app.put("/update_profile")
def update_profile(profile: ProfileUpdate):
    if profile.username not in fake_user_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = fake_user_db[profile.username]

    # Update fields if provided
    if profile.email is not None:
        user_data["email"] = profile.email
    if profile.birthdate is not None:
        user_data["birthdate"] = profile.birthdate.isoformat()
    if profile.gender is not None:
        user_data["gender"] = profile.gender
    if profile.city is not None:
        user_data["city"] = profile.city
    if profile.profession is not None:
        user_data["profession"] = profile.profession
    if profile.interests is not None:
        user_data["interests"] = profile.interests
    if profile.social_links is not None:
        user_data["social_links"] = profile.social_links.dict()
    if profile.bio is not None:
        user_data["bio"] = profile.bio

    return {"message": "Profile updated successfully", "updated_profile": user_data}
