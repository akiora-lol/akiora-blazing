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
    avatar: Optional[str] = None
    description: Optional[str] = None
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
    actor_id: Optional[UUID] = None
    user_id: UUID
    tokens: List[str] = Field(default_factory=list)


class RemoveMemberRequest(BaseModel):
    club_id: UUID
    actor_id: Optional[UUID] = None
    user_id: UUID


class SetPermissionRequest(BaseModel):
    club_id: UUID
    actor_id: UUID
    target_user_id: UUID
    tokens: List[str] = Field(default_factory=list)


class PaginationRequest(BaseModel):
    page: int = 1
    page_size: int = 50


class ClubFilter(BaseModel):
    search: Optional[str] = None
    owner_id: Optional[UUID] = None
    is_member: bool = False


class ListClubsRequest(BaseModel):
    filter: ClubFilter = Field(default_factory=ClubFilter)
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class ListClubsResponse(BaseModel):
    clubs: List[ClubResponse] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 50
    has_next: bool = False


class DeleteClubRequest(BaseModel):
    club_id: UUID
    actor_id: UUID


class MemberInfo(BaseModel):
    user_id: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    permissions: ClubPermission = Field(default_factory=ClubPermission)


class ClubMembersResponse(BaseModel):
    members: List[MemberInfo] = Field(default_factory=list)
    total_count: int = 0


class GetMembersRequest(BaseModel):
    club_id: UUID
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class SearchMembersRequest(BaseModel):
    club_id: UUID
    search: Optional[str] = None
    pagination: PaginationRequest = Field(default_factory=PaginationRequest)


class GetMemberPermissionsRequest(BaseModel):
    club_id: UUID
    user_id: UUID


class MemberPermissionResponse(BaseModel):
    user_id: str
    tokens: List[str] = Field(default_factory=list)


class IsMemberRequest(BaseModel):
    club_id: UUID
    user_id: UUID


class IsMemberResponse(BaseModel):
    is_member: bool = False
    role: Optional[str] = None
    permissions: ClubPermission = Field(default_factory=ClubPermission)
