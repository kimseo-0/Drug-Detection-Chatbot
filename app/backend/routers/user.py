from fastapi import APIRouter, HTTPException
from models.schemas import UserProfile, UserProfileCreate
from infra import db

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/info", response_model=UserProfile)
def save_user_info(profile: UserProfileCreate):
    """사용자 정보 저장/갱신"""
    saved = db.save_user_profile(profile)
    return saved

@router.get("/info/{user_id}", response_model=UserProfile)
def get_user_info(user_id: str):
    """사용자 정보 조회"""
    profile = db.get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.delete("/info/{user_id}")
def delete_user_info(user_id: str):
    """사용자 정보 삭제"""
    deleted = db.delete_user_profile(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted", "user_id": user_id}
