from typing import Optional, Dict
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import UUID


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNSPECIFIED = "UNSPECIFIED"


class UserType(str, Enum):
    DEFAULT = "DEFAULT"
    STAFF = "STAFF"
    STREAMER = "STREAMER"
    PRO = "PRO"
    MODERATOR = "MODERATOR"
    UNSPECIFIED = "UNSPECIFIED"


class Social(BaseModel):
    link: str
    hidden: bool = False


class Birthday(BaseModel):
    day: str  # Format: YYYY-MM-DD
    hidden: bool = False

    @field_validator("day")
    @classmethod
    def validate_date_format(cls, v: str):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Birthday must be in YYYY-MM-DD format")
        return v


class CreateUserRequest(BaseModel):
    email: EmailStr
    nickname: Optional[str] = None


class GetUserRequest(BaseModel):
    id: UUID


class GetUserByEmailRequest(BaseModel):
    email: EmailStr


class UpdateUserRequest(BaseModel):
    user_id: UUID
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = Field(None, max_length=500)
    gender: Gender = Gender.UNSPECIFIED
    user_type: UserType = UserType.UNSPECIFIED
    birth_date: Optional[Birthday] = None
    socials: Dict[str, Social] = Field(default_factory=dict)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str
    user_type: UserType
    avatar: Optional[str] = None
    bio: Optional[str] = None
    gender: Gender
    birth_date: Optional[Birthday] = None
    socials: Dict[str, Social] = Field(default_factory=dict)
    created_at: int
    last_updated: int

    class Config:
        from_attributes = True
