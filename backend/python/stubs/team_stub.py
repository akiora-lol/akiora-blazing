import grpc
from uuid import UUID

from shared.contracts.team import (
    TeamResponse,
    CreateTeamRequest,
    GetTeamRequest,
    UpdateTeamRequest,
    AddTeamMemberRequest,
    RemoveTeamMemberRequest,
)

import community.team.v1.team_service_pb2 as pb2_module
import community.team.v1.team_service_pb2_grpc as pb2_grpc_module


class TeamMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Team service"""

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> TeamResponse:
        return TeamResponse(
            id=UUID(grpc_response.id),
            owner_id=UUID(grpc_response.owner_id),
            name=grpc_response.name,
            avatar=grpc_response.avatar if grpc_response.avatar else None,
            tag=grpc_response.tag,
            members=list(grpc_response.members),
            created_at=grpc_response.created_at,
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateTeamRequest):
        return pb2_module.CreateTeamRequest(
            owner_id=str(request.owner_id),
            name=request.name,
            tag=request.tag,
        )

    @classmethod
    def to_grpc_get_request(cls, request: GetTeamRequest):
        return pb2_module.GetTeamRequest(team_id=str(request.team_id))

    @classmethod
    def to_grpc_update_request(cls, request: UpdateTeamRequest):
        grpc_request = pb2_module.UpdateTeamRequest(
            team_id=str(request.team_id),
            actor_id=str(request.actor_id),
        )
        if request.name:
            grpc_request.name = request.name
        if request.avatar:
            grpc_request.avatar = request.avatar
        if request.tag:
            grpc_request.tag = request.tag
        return grpc_request

    @classmethod
    def to_grpc_add_member_request(cls, request: AddTeamMemberRequest):
        return pb2_module.AddTeamMemberRequest(
            team_id=str(request.team_id),
            actor_id=str(request.actor_id),
            user_id=str(request.user_id),
        )

    @classmethod
    def to_grpc_remove_member_request(cls, request: RemoveTeamMemberRequest):
        return pb2_module.RemoveTeamMemberRequest(
            team_id=str(request.team_id),
            actor_id=str(request.actor_id),
            user_id=str(request.user_id),
        )


class TeamStub:
    """Stub for Team Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.TeamServiceStub(channel)
        self.mapper = TeamMapper()

    async def create_team(self, request: CreateTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_team(self, request: GetTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_team(self, request: UpdateTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_update_request(request)
        response = await self.stub.UpdateTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def add_member(self, request: AddTeamMemberRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_add_member_request(request)
        response = await self.stub.AddMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def remove_member(self, request: RemoveTeamMemberRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_remove_member_request(request)
        response = await self.stub.RemoveMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def create_team_sync(self, request: CreateTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_team_sync(self, request: GetTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)
