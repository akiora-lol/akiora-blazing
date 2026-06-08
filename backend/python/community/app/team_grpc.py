import grpc
from uuid import UUID
from loguru import logger

from dishka.integrations.grpcio import inject

from domain.services.team_service import TeamService
from domain.entites.team import MAX_TEAM_SIZE, Team
from domain.entites.user import User


def _paginate(items, pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, page_size, end < len(items)


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
        if request.HasField("avatar"):
            await team.update({"$set": {"avatar": request.avatar}})
            team = await Team.get(team.id)
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
        from community.team.v1 import team_service_pb2 as pb2
        team = await TeamService.remove_member(
            team_id=UUID(request.team_id),
            actor_id=UUID(request.actor_id),
            user_id=UUID(request.user_id),
        )
        return _team_to_proto(team, pb2)

    @inject
    async def DeleteTeam(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        team = await Team.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        if UUID(request.actor_id) != team.owner_id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only owner can delete team")
        await team.delete()
        return Empty()

    @inject
    async def ListTeams(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        teams = await Team.find_all().to_list()
        if request.HasField("filter"):
            filter_ = request.filter
            if filter_.search:
                teams = [
                    team for team in teams
                    if filter_.search.lower() in team.name.lower()
                    or (team.tag and filter_.search.lower() in team.tag.lower())
                ]
            if filter_.owner_id:
                owner_id = UUID(filter_.owner_id)
                teams = [team for team in teams if team.owner_id == owner_id]
            if filter_.is_member and filter_.owner_id:
                user_id = UUID(filter_.owner_id)
                teams = [team for team in teams if user_id in team.members]
        page_items, page, page_size, has_next = _paginate(teams, request.pagination)
        return pb2.ListTeamsResponse(
            teams=[_team_to_proto(team, pb2) for team in page_items],
            total_count=len(teams),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

    @inject
    async def GetMembers(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        team = await Team.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        members, _, _, _ = _paginate(team.members, request.pagination)
        return await _team_members_to_proto(team, members, pb2)

    @inject
    async def SearchMembers(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        team = await Team.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        matched = []
        for member_id in team.members:
            user = await User.get(member_id)
            if not request.search or (
                user and request.search.lower() in user.nickname.lower()
            ):
                matched.append(member_id)
        members, _, _, _ = _paginate(matched, request.pagination)
        return await _team_members_to_proto(team, members, pb2, total_count=len(matched))

    @inject
    async def CheckCapacity(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        team = await Team.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        return pb2.CheckCapacityResponse(
            can_add=not team.is_full(),
            current_members=len(team.members),
            max_members=MAX_TEAM_SIZE,
        )

    @inject
    async def IsMember(self, request, context: grpc.aio.ServicerContext):
        from community.team.v1 import team_service_pb2 as pb2
        team = await Team.get(UUID(request.team_id))
        if not team:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Team not found")
        user_id = UUID(request.user_id)
        return pb2.IsMemberResponse(
            is_member=user_id in team.members,
            role="owner" if user_id == team.owner_id else "member",
        )


async def _team_members_to_proto(team: Team, members, pb2, total_count: int | None = None):
    infos = []
    for member_id in members:
        user = await User.get(member_id)
        infos.append(
            pb2.MemberInfo(
                user_id=str(member_id),
                nickname=user.nickname if user else "",
                avatar=user.avatar if user and user.avatar else "",
            )
        )
    return pb2.TeamMembersResponse(
        members=infos,
        total_count=total_count if total_count is not None else len(team.members),
    )
