import grpc
from uuid import UUID
from typing import Dict

from shared.contracts.club import (
    ClubResponse,
    CreateClubRequest,
    GetClubRequest,
    UpdateClubRequest,
    AddMemberRequest,
    RemoveMemberRequest,
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
    def to_grpc_create_request(cls, request: CreateClubRequest):
        grpc_request = pb2_module.CreateClubRequest(
            owner_id=str(request.owner_id),
            name=request.name,
        )
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
            user_id=str(request.user_id),
            tokens=request.tokens,
        )

    @classmethod
    def to_grpc_remove_member_request(cls, request: RemoveMemberRequest):
        return pb2_module.RemoveMemberRequest(
            club_id=str(request.club_id),
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

    def create_club_sync(self, request: CreateClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateClub(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_club_sync(self, request: GetClubRequest) -> ClubResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetClub(grpc_request)
        return self.mapper.to_pydantic_response(response)
