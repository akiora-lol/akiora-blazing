from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID


class TeamResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    avatar: Optional[str] = None
    tag: str
    members: List[str] = Field(default_factory=list)
    created_at: int

    class Config:
        from_attributes = True


class CreateTeamRequest(BaseModel):
    owner_id: UUID
    name: str
    tag: str


class GetTeamRequest(BaseModel):
    team_id: UUID


class UpdateTeamRequest(BaseModel):
    team_id: UUID
    actor_id: UUID
    name: Optional[str] = None
    avatar: Optional[str] = None
    tag: Optional[str] = None


class AddTeamMemberRequest(BaseModel):
    team_id: UUID
    actor_id: UUID
    user_id: UUID


class RemoveTeamMemberRequest(BaseModel):
    team_id: UUID
    actor_id: UUID
    user_id: UUID
