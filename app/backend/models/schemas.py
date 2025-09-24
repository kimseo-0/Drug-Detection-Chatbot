from pydantic import BaseModel
from typing import List, Optional

#  사용자 정보 등록/수정 시 요청 바디
class UserProfileCreate(BaseModel):
    user_id: str
    disease: Optional[str] = None                # 질병
    caution_drugs: List[str] = []                # 주의 약품
    caution_ingredients: List[str] = []          # 주의 성분
    current_medications: List[str] = []          # 복용 중인 약

#  사용자 정보 조회/응답
class UserProfile(BaseModel):
    user_id: str
    disease: Optional[str] = None
    caution_drugs: List[str] = []
    caution_ingredients: List[str] = []
    current_medications: List[str] = []

    # class Config:
    #     orm_mode = True   # DB ORM 객체를 바로 반환할 때도 대응 가능
