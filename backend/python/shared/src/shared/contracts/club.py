from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from uuid import UUID


class ClubPermission(BaseModel):
    tokens: List[str] = Field(default_factory=list)


class FieldGroup(BaseModel):
    fields: List[str] = Field(default_factory=list)


class ClubResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    members: List[str] = Field(default_factory=list)
    fields: List[FieldGroup] = Field(default_factory=list)
    permissions: Dict[str, ClubPermission] = Field(default_factory=dict)
    created_at: int

    class Config:
        from_attributes = True


class CreateClubRequest(BaseModel):
    owner_id: UUID
    name: str
    fields: List[FieldGroup] = Field(default_factory=list)


class GetClubRequest(BaseModel):
    club_id: UUID


class UpdateClubRequest(BaseModel):
    club_id: UUID
    actor_id: UUID
    name: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    fields: List[FieldGroup] = Field(default_factory=list)


class AddMemberRequest(BaseModel):
    club_id: UUID
    user_id: UUID
    tokens: List[str] = Field(default_factory=list)


class RemoveMemberRequest(BaseModel):
    club_id: UUID
    user_id: UUID


class SetPermissionRequest(BaseModel):
    club_id: UUID
    actor_id: UUID
    target_user_id: UUID
    tokens: List[str] = Field(default_factory=list)
