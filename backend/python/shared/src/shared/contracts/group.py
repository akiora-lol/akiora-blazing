from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


class GroupResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    users: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreateGroupRequest(BaseModel):
    owner_id: UUID
    name: str


class GetGroupRequest(BaseModel):
    id: UUID


class PatchGroupRequest(BaseModel):
    owner_id: UUID
    name: Optional[str] = None
    add_users: List[str] = Field(default_factory=list)
    delete_users: List[str] = Field(default_factory=list)
