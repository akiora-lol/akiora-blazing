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
    avatar: Optional[str] = None


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


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 50


class TeamFilter(BaseModel):
    search: Optional[str] = None
    owner_id: Optional[UUID] = None
    is_member: bool = False


class ListTeamsRequest(BaseModel):
    filter: TeamFilter = Field(default_factory=TeamFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListTeamsResponse(BaseModel):
    teams: List[TeamResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class DeleteTeamRequest(BaseModel):
    team_id: UUID
    actor_id: UUID


class MemberInfo(BaseModel):
    user_id: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class TeamMembersResponse(BaseModel):
    members: List[MemberInfo] = Field(default_factory=list)
    total_count: int = 0


class GetMembersRequest(BaseModel):
    team_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class SearchMembersRequest(BaseModel):
    team_id: UUID
    search: Optional[str] = None
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class CheckCapacityRequest(BaseModel):
    team_id: UUID


class CheckCapacityResponse(BaseModel):
    can_add: bool = False
    current_members: int = 0
    max_members: int = 0


class IsMemberRequest(BaseModel):
    team_id: UUID
    user_id: UUID


class IsMemberResponse(BaseModel):
    is_member: bool = False
    role: Optional[str] = None
