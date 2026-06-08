import grpc
from uuid import UUID
from typing import Dict

from shared.contracts.club import (
    ClubMembersResponse,
    ClubResponse,
    CreateClubRequest,
    DeleteClubRequest,
    GetClubRequest,
    GetMemberPermissionsRequest,
    GetMembersRequest,
    IsMemberRequest,
    IsMemberResponse,
    ListClubsRequest,
    ListClubsResponse,
    MemberInfo,
    MemberPermissionResponse,
    UpdateClubRequest,
    AddMemberRequest,
    RemoveMemberRequest,
    SearchMembersRequest,
    SetPermissionRequest,
    ClubPermission,
    FieldGroup,
)

import community.club.v1.club_service_pb2 as pb2_module
import community.club.v1.club_service_pb2_grpc as pb2_grpc_module


class ClubMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Club service"""

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> ClubResponse:
        """Convert gRPC ClubResponse to Pydantic ClubResponse"""
        members = list(grpc_response.members)

        fields = []
        for fg in grpc_response.fields:
            fields.append(FieldGroup(fields=list(fg.fields)))

        permissions: Dict[str, ClubPermission] = {}
        for key, perm in grpc_response.permissions.items():
            permissions[key] = ClubPermission(tokens=list(perm.tokens))

        return ClubResponse(
            id=UUID(grpc_response.id),
            owner_id=UUID(grpc_response.owner_id),
            name=grpc_response.name,
            avatar=grpc_response.avatar if grpc_response.avatar else None,
            description=grpc_response.description if grpc_response.description else None,
            members=members,
            fields=fields,
            permissions=permissions,
            created_at=grpc_response.created_at,
        )

    @classmethod
    def to_pydantic_list_response(cls, grpc_response) -> ListClubsResponse:
        return ListClubsResponse(
            clubs=[cls.to_pydantic_response(club) for club in grpc_response.clubs],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_members_response(cls, grpc_response) -> ClubMembersResponse:
        return ClubMembersResponse(
            members=[
                MemberInfo(
                    user_id=member.user_id,
                    nickname=member.nickname or None,
                    avatar=member.avatar or None,
                    permissions=ClubPermission(tokens=list(member.permissions.tokens)),
                )
                for member in grpc_response.members
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateClubRequest):
        grpc_request = pb2_module.CreateClubRequest(
            owner_id=str(request.owner_id),
            name=request.name,
        )
        if request.avatar:
            grpc_request.avatar = request.avatar
        if request.description:
            grpc_request.description = request.description
        for fg in request.fields:
            field_group = pb2_module.FieldGroup(fields=fg.fields)
            grpc_request.fields.append(field_group)
        return grpc_request

    @classmethod
    def to_grpc_get_request(cls, request: GetClubRequest):
        return pb2_module.GetClubRequest(club_id=str(request.club_id))

    @classmethod
    def to_grpc_update_request(cls, request: UpdateClubRequest):
        grpc_request = pb2_module.UpdateClubRequest(
            club_id=str(request.club_id),
            actor_id=str(request.actor_id),
        )
        if request.name:
            grpc_request.name = request.name
        if request.avatar:
            grpc_request.avatar = request.avatar
        if request.description:
            grpc_request.description = request.description
        for fg in request.fields:
            field_group = pb2_module.FieldGroup(fields=fg.fields)
            grpc_request.fields.append(field_group)
        return grpc_request

    @classmethod
    def to_grpc_add_member_request(cls, request: AddMemberRequest):
        return pb2_module.AddMemberRequest(
            club_id=str(request.club_id),
            actor_id=str(request.actor_id or ""),
            user_id=str(request.user_id),
            tokens=request.tokens,
        )

    @classmethod
    def to_grpc_remove_member_request(cls, request: RemoveMemberRequest):
        return pb2_module.RemoveMemberRequest(
            club_id=str(request.club_id),
            actor_id=str(request.actor_id or ""),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_set_permission_request(cls, request: SetPermissionRequest):
        return pb2_module.SetPermissionRequest(
            club_id=str(request.club_id),
            actor_id=str(request.actor_id),
            target_user_id=str(request.target_user_id),
            tokens=request.tokens,
        )

    @classmethod
    def to_grpc_delete_request(cls, request: DeleteClubRequest):
        return pb2_module.DeleteClubRequest(
            club_id=str(request.club_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_list_request(cls, request: ListClubsRequest):
        grpc_filter = pb2_module.ClubFilter(is_member=request.filter.is_member)
        if request.filter.search:
            grpc_filter.search = request.filter.search
        if request.filter.owner_id:
            grpc_filter.owner_id = str(request.filter.owner_id)
        return pb2_module.ListClubsRequest(
            filter=grpc_filter,
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_get_members_request(cls, request: GetMembersRequest):
        return pb2_module.GetMembersRequest(
            club_id=str(request.club_id),
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_search_members_request(cls, request: SearchMembersRequest):
        return pb2_module.SearchMembersRequest(
            club_id=str(request.club_id),
            search=request.search or "",
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_get_member_permissions_request(
        cls, request: GetMemberPermissionsRequest
    ):
        return pb2_module.GetMemberPermissionsRequest(
            club_id=str(request.club_id),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_is_member_request(cls, request: IsMemberRequest):
        return pb2_module.IsMemberRequest(
            club_id=str(request.club_id),
            user_id=str(request.user_id),
        )


class ClubStub:
    """Stub for Club Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.ClubServiceStub(channel)
        self.mapper = ClubMapper()

    async def create_club(self, request: CreateClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateClub(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_club(self, request: GetClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetClub(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_club(self, request: UpdateClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_update_request(request)
        response = await self.stub.UpdateClub(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def delete_club(self, request: DeleteClubRequest):
        grpc_request = self.mapper.to_grpc_delete_request(request)
        return await self.stub.DeleteClub(grpc_request)

    async def list_clubs(self, request: ListClubsRequest) -> ListClubsResponse:
        grpc_request = self.mapper.to_grpc_list_request(request)
        response = await self.stub.ListClubs(grpc_request)
        return self.mapper.to_pydantic_list_response(response)

    async def add_member(self, request: AddMemberRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_add_member_request(request)
        response = await self.stub.AddMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def remove_member(self, request: RemoveMemberRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_remove_member_request(request)
        response = await self.stub.RemoveMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def set_permission(self, request: SetPermissionRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_set_permission_request(request)
        response = await self.stub.SetPermission(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_members(self, request: GetMembersRequest) -> ClubMembersResponse:
        grpc_request = self.mapper.to_grpc_get_members_request(request)
        response = await self.stub.GetMembers(grpc_request)
        return self.mapper.to_pydantic_members_response(response)

    async def search_members(
        self, request: SearchMembersRequest
    ) -> ClubMembersResponse:
        grpc_request = self.mapper.to_grpc_search_members_request(request)
        response = await self.stub.SearchMembers(grpc_request)
        return self.mapper.to_pydantic_members_response(response)

    async def get_member_permissions(
        self, request: GetMemberPermissionsRequest
    ) -> MemberPermissionResponse:
        grpc_request = self.mapper.to_grpc_get_member_permissions_request(request)
        response = await self.stub.GetMemberPermissions(grpc_request)
        return MemberPermissionResponse(
            user_id=response.user_id,
            tokens=list(response.tokens),
        )

    async def is_member(self, request: IsMemberRequest) -> IsMemberResponse:
        grpc_request = self.mapper.to_grpc_is_member_request(request)
        response = await self.stub.IsMember(grpc_request)
        return IsMemberResponse(
            is_member=response.is_member,
            role=response.role or None,
            permissions=ClubPermission(tokens=list(response.permissions.tokens)),
        )

    def create_club_sync(self, request: CreateClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateClub(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_club_sync(self, request: GetClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetClub(grpc_request)
        return self.mapper.to_pydantic_response(response)
