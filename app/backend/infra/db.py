import json
import os
from models.schemas import UserProfileCreate, UserProfile

DB_FILE = "user_db.json"

# DB 파일이 없으면 빈 dict로 초기화
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def _load_db() -> dict:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_user_profile(profile: UserProfileCreate) -> UserProfile:
    data = _load_db()
    data[profile.user_id] = profile.dict()
    _save_db(data)
    return UserProfile(**data[profile.user_id])

def get_user_profile(user_id: str) -> UserProfile | None:
    data = _load_db()
    if user_id not in data:
        return None
    return UserProfile(**data[user_id])

def delete_user_profile(user_id: str) -> dict | None:
    data = _load_db()
    if user_id not in data:
        return None
    deleted = data.pop(user_id)
    _save_db(data)
    return deleted
