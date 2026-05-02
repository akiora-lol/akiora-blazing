import grpc
from uuid import UUID
from loguru import logger

from dishka.integrations.grpcio import inject

from domain.services.team_service import TeamService
from domain.entites.team import Team


def _team_to_proto(team: Team, pb2):
    return pb2.TeamResponse(
        id=str(team.id),
        owner_id=str(team.owner_id),
        name=team.name,
        avatar=team.avatar or "",
        tag=team.tag or "",
        members=[str(m) for m in team.members],
        created_at=int(team.created_at.timestamp()),
    )


class TeamGrpc:
    @inject
    async def CreateTeam(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        logger.debug("CreateTeam owner={}", request.owner_id)
        team = await TeamService.create(
            owner_id=UUID(request.owner_id),
            name=request.name,
            tag=request.tag if request.HasField("tag") else None,
        )
        return _team_to_proto(team, pb2)

    @inject
    async def GetTeam(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        logger.debug("GetTeam id={}", request.team_id)
        team = await TeamService.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        return _team_to_proto(team, pb2)

    @inject
    async def UpdateTeam(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        logger.debug("UpdateTeam id={}", request.team_id)
        team = await TeamService.update(
            team_id=UUID(request.team_id),
            actor_id=UUID(request.actor_id),
            name=request.name if request.HasField("name") else None,
            avatar=request.avatar if request.HasField("avatar") else None,
            tag=request.tag if request.HasField("tag") else None,
        )
        return _team_to_proto(team, pb2)

    @inject
    async def AddMember(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        logger.debug("AddMember team={} user={}", request.team_id, request.user_id)
        team = await TeamService.add_member(
            team_id=UUID(request.team_id),
            actor_id=UUID(request.actor_id),
            user_id=UUID(request.user_id),
        )
        return _team_to_proto(team, pb2)

    @inject
    async def RemoveMember(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        await TeamService.remove_member(
            team_id=UUID(request.team_id),
            actor_id=UUID(request.actor_id),
            user_id=UUID(request.user_id),
        )
        return Empty()
