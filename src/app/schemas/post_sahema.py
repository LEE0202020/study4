from pydantic import BaseModel
from datetime import datetime
from app.schemas.member_schema import MemberSummeryDTO


# VO
class PostVO(BaseModel):
    id: int
    post_title: str
    post_content: str
    post_read_count: int
    post_updated_at: datetime | None = None #수정일
    post_created_at: datetime | None = None
    member_id: int

# DTO
class PostCreateDTO(BaseModel):
    post_title: str
    post_content: str

    class Config: 
        from_attributes = True


# DTO
class PostDatailResponseDTO(BaseModel):
    id: int
    post_title: str
    post_content: str
    post_read_count: int
    post_updated_at: datetime | None = None 
    post_created_at: datetime | None = None

    member: MemberSummeryDTO


    class Config: 
        from_attributes = True


# DTO
class PostListReaponseDTO(BaseModel):
    id: int
    post_title: str
    post_read_count: int
    post_updated_at: datetime | None = None 
    post_created_at: datetime | None = None

    member: MemberSummeryDTO


    class Config: 
        from_attributes = True