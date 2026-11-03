from pydantic import BaseModel
from datetime import datetime
from app.enums.member_enum import MemberProvider

# VO
class MemberVO(BaseModel):
    id: int
    member_email: str
    member_password: str | None = None
    member_name: str | None = None
    member_age: int | None = None
    member_profile: str | None = "/members/default.jpg"
    member_provider_id: str | None = None
    member_provider: MemberProvider
    member_created_at: datetime | None = None


# DTO
class MemberCreateDTO(BaseModel):
    member_email: str
    member_password: str | None = None
    member_name: str | None = None
    member_age: int | None = None
    member_profile: str | None = "/members/default.jpg"
    member_provider: MemberProvider