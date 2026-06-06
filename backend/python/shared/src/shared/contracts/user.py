from typing import Optional, Dict, List
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


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 50
    before_timestamp: Optional[int] = None


class UserFilter(BaseModel):
    search: Optional[str] = None
    user_type: Optional[UserType] = None
    gender: Optional[Gender] = None
    has_avatar: bool = False
    min_created_at: Optional[int] = None
    max_created_at: Optional[int] = None


class ListUsersRequest(BaseModel):
    filter: UserFilter = Field(default_factory=UserFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListUsersResponse(BaseModel):
    users: List[UserResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class DeleteUserRequest(BaseModel):
    user_id: UUID
    actor_id: UUID


class FriendRequest(BaseModel):
    sender_id: UUID
    receiver_id: UUID


class RespondFriendRequest(BaseModel):
    request_id: UUID
    responder_id: UUID
    accept: bool = False


class FriendResponse(BaseModel):
    id: UUID
    user_id_1: UUID
    user_id_2: UUID
    status: str
    created_at: int
    updated_at: int


class SendFriendRequestRequest(BaseModel):
    request: FriendRequest


class RespondFriendRequestRequest(BaseModel):
    response: RespondFriendRequest


class ListFriendsRequest(BaseModel):
    user_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)
    status: str = "ALL"


class ListFriendsResponse(BaseModel):
    friends: List[FriendResponse] = Field(default_factory=list)
    total_count: int = 0


class RemoveFriendRequest(BaseModel):
    user_id_1: UUID
    user_id_2: UUID
    actor_id: UUID


class BlockUserRequest(BaseModel):
    blocker_id: UUID
    blocked_id: UUID


class UnblockUserRequest(BaseModel):
    blocker_id: UUID
    blocked_id: UUID


class GetFriendStatusRequest(BaseModel):
    user_id_1: UUID
    user_id_2: UUID


class GetFriendStatusResponse(BaseModel):
    status: str
    request_id: Optional[UUID] = None
