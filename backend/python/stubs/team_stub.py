import grpc
from uuid import UUID

from shared.contracts.team import (
    TeamResponse,
    CreateTeamRequest,
    CheckCapacityRequest,
    CheckCapacityResponse,
    DeleteTeamRequest,
    GetMembersRequest,
    GetTeamRequest,
    IsMemberRequest,
    IsMemberResponse,
    ListTeamsRequest,
    ListTeamsResponse,
    MemberInfo,
    SearchMembersRequest,
    TeamMembersResponse,
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
    def to_pydantic_list_response(cls, grpc_response) -> ListTeamsResponse:
        return ListTeamsResponse(
            teams=[cls.to_pydantic_response(team) for team in grpc_response.teams],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_members_response(cls, grpc_response) -> TeamMembersResponse:
        return TeamMembersResponse(
            members=[
                MemberInfo(
                    user_id=member.user_id,
                    nickname=member.nickname or None,
                    avatar=member.avatar or None,
                )
                for member in grpc_response.members
            ],
            total_count=grpc_response.total_count,
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateTeamRequest):
        return pb2_module.CreateTeamRequest(
            owner_id=str(request.owner_id),
            name=request.name,
            avatar=request.avatar or "",
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

    @classmethod
    def to_grpc_delete_request(cls, request: DeleteTeamRequest):
        return pb2_module.DeleteTeamRequest(
            team_id=str(request.team_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_list_request(cls, request: ListTeamsRequest):
        grpc_filter = pb2_module.TeamFilter(is_member=request.filter.is_member)
        if request.filter.search:
            grpc_filter.search = request.filter.search
        if request.filter.owner_id:
            grpc_filter.owner_id = str(request.filter.owner_id)
        return pb2_module.ListTeamsRequest(
            filter=grpc_filter,
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_get_members_request(cls, request: GetMembersRequest):
        return pb2_module.GetMembersRequest(
            team_id=str(request.team_id),
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_search_members_request(cls, request: SearchMembersRequest):
        return pb2_module.SearchMembersRequest(
            team_id=str(request.team_id),
            search=request.search or "",
            pagination=pb2_module.PaginationRequest(
                page=request.pagination.page,
                page_size=request.pagination.page_size,
            ),
        )

    @classmethod
    def to_grpc_check_capacity_request(cls, request: CheckCapacityRequest):
        return pb2_module.CheckCapacityRequest(team_id=str(request.team_id))

    @classmethod
    def to_grpc_is_member_request(cls, request: IsMemberRequest):
        return pb2_module.IsMemberRequest(
            team_id=str(request.team_id),
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

    async def delete_team(self, request: DeleteTeamRequest):
        grpc_request = self.mapper.to_grpc_delete_request(request)
        return await self.stub.DeleteTeam(grpc_request)

    async def list_teams(self, request: ListTeamsRequest) -> ListTeamsResponse:
        grpc_request = self.mapper.to_grpc_list_request(request)
        response = await self.stub.ListTeams(grpc_request)
        return self.mapper.to_pydantic_list_response(response)

    async def add_member(self, request: AddTeamMemberRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_add_member_request(request)
        response = await self.stub.AddMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def remove_member(self, request: RemoveTeamMemberRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_remove_member_request(request)
        response = await self.stub.RemoveMember(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_members(self, request: GetMembersRequest) -> TeamMembersResponse:
        grpc_request = self.mapper.to_grpc_get_members_request(request)
        response = await self.stub.GetMembers(grpc_request)
        return self.mapper.to_pydantic_members_response(response)

    async def search_members(
        self, request: SearchMembersRequest
    ) -> TeamMembersResponse:
        grpc_request = self.mapper.to_grpc_search_members_request(request)
        response = await self.stub.SearchMembers(grpc_request)
        return self.mapper.to_pydantic_members_response(response)

    async def check_capacity(
        self, request: CheckCapacityRequest
    ) -> CheckCapacityResponse:
        grpc_request = self.mapper.to_grpc_check_capacity_request(request)
        response = await self.stub.CheckCapacity(grpc_request)
        return CheckCapacityResponse(
            can_add=response.can_add,
            current_members=response.current_members,
            max_members=response.max_members,
        )

    async def is_member(self, request: IsMemberRequest) -> IsMemberResponse:
        grpc_request = self.mapper.to_grpc_is_member_request(request)
        response = await self.stub.IsMember(grpc_request)
        return IsMemberResponse(
            is_member=response.is_member,
            role=response.role or None,
        )

    def create_team_sync(self, request: CreateTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_team_sync(self, request: GetTeamRequest) -> TeamResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetTeam(grpc_request)
        return self.mapper.to_pydantic_response(response)
