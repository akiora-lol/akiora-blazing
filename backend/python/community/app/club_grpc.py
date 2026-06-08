import grpc
from uuid import UUID
from loguru import logger

from dishka.integrations.grpcio import inject

from domain.services.club_service import ClubService
from domain.entites.club import Club, ClubPermission
from domain.entites.user import User


def _paginate(items, pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, page_size, end < len(items)


def _club_to_proto(club: Club, pb2):
    fields = [pb2.FieldGroup(fields=fg) for fg in club.fields]
    permissions = {
        uid: pb2.ClubPermission(tokens=perm.tokens)
        for uid, perm in club.permissions.items()
    }
    return pb2.ClubResponse(
        id=str(club.id),
        owner_id=str(club.owner_id),
        name=club.name,
        avatar=club.avatar or "",
        description=club.description or "",
        members=[str(m) for m in club.members],
        fields=fields,
        permissions=permissions,
        created_at=int(club.created_at.timestamp()),
    )


class ClubGrpc:
    @inject
    async def CreateClub(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        logger.debug("CreateClub owner={}", request.owner_id)
        fields = [list(fg.fields) for fg in request.fields]
        club = await ClubService.create(
            owner_id=UUID(request.owner_id),
            name=request.name,
            fields=fields,
        )
        patch = {}
        if request.HasField("avatar"):
            patch["avatar"] = request.avatar
        if request.HasField("description"):
            patch["description"] = request.description
        if patch:
            await club.update({"$set": patch})
            club = await Club.get(club.id)
        return _club_to_proto(club, pb2)

    @inject
    async def GetClub(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        logger.debug("GetClub id={}", request.club_id)
        club = await ClubService.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        return _club_to_proto(club, pb2)

    @inject
    async def UpdateClub(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        logger.debug("UpdateClub id={}", request.club_id)
        fields = [list(fg.fields) for fg in request.fields] if request.fields else None
        club = await ClubService.update(
            club_id=UUID(request.club_id),
            actor_id=UUID(request.actor_id),
            name=request.name if request.HasField("name") else None,
            avatar=request.avatar if request.HasField("avatar") else None,
            description=request.description if request.HasField("description") else None,
            fields=fields,
        )
        return _club_to_proto(club, pb2)

    @inject
    async def AddMember(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        logger.debug("AddMember club={} user={}", request.club_id, request.user_id)
        club = await ClubService.add_member(
            club_id=UUID(request.club_id),
            user_id=UUID(request.user_id),
            tokens=list(request.tokens) or None,
        )
        return _club_to_proto(club, pb2)

    @inject
    async def RemoveMember(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        logger.debug("RemoveMember club={} user={}", request.club_id, request.user_id)
        club = await ClubService.remove_member(
            club_id=UUID(request.club_id),
            user_id=UUID(request.user_id),
        )
        return _club_to_proto(club, pb2)

    @inject
    async def SetPermission(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await ClubService.set_permission(
            club_id=UUID(request.club_id),
            actor_id=UUID(request.actor_id),
            target_user_id=UUID(request.target_user_id),
            tokens=list(request.tokens),
        )
        return _club_to_proto(club, pb2)

    @inject
    async def DeleteClub(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        club = await Club.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        if request.actor_id and UUID(request.actor_id) != club.owner_id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only owner can delete club")
        await club.delete()
        return Empty()

    @inject
    async def ListClubs(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        clubs = await Club.find_all().to_list()
        if request.HasField("filter"):
            filter_ = request.filter
            if filter_.search:
                clubs = [
                    club for club in clubs
                    if filter_.search.lower() in club.name.lower()
                    or (club.description and filter_.search.lower() in club.description.lower())
                ]
            if filter_.owner_id:
                owner_id = UUID(filter_.owner_id)
                clubs = [club for club in clubs if club.owner_id == owner_id]
            if filter_.is_member and filter_.owner_id:
                user_id = UUID(filter_.owner_id)
                clubs = [club for club in clubs if user_id in club.members]
        page_items, page, page_size, has_next = _paginate(clubs, request.pagination)
        return pb2.ListClubsResponse(
            clubs=[_club_to_proto(club, pb2) for club in page_items],
            total_count=len(clubs),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

    @inject
    async def GetMembers(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await Club.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        members, _, _, _ = _paginate(club.members, request.pagination)
        return await _club_members_to_proto(club, members, pb2)

    @inject
    async def SearchMembers(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await Club.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        matched = []
        for member_id in club.members:
            user = await User.get(member_id)
            if not request.search or (
                user and request.search.lower() in user.nickname.lower()
            ):
                matched.append(member_id)
        members, _, _, _ = _paginate(matched, request.pagination)
        return await _club_members_to_proto(club, members, pb2, total_count=len(matched))

    @inject
    async def GetMemberPermissions(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await Club.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        permission = club.permissions.get(str(request.user_id), ClubPermission())
        return pb2.MemberPermissionResponse(
            user_id=request.user_id,
            tokens=permission.tokens,
        )

    @inject
    async def IsMember(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await Club.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        user_id = UUID(request.user_id)
        permission = club.permissions.get(str(user_id), ClubPermission())
        return pb2.IsMemberResponse(
            is_member=user_id in club.members,
            role="owner" if user_id == club.owner_id else "member",
            permissions=pb2.ClubPermission(tokens=permission.tokens),
        )


async def _club_members_to_proto(club: Club, members, pb2, total_count: int | None = None):
    infos = []
    for member_id in members:
        user = await User.get(member_id)
        permission = club.permissions.get(str(member_id), ClubPermission())
        infos.append(
            pb2.MemberInfo(
                user_id=str(member_id),
                nickname=user.nickname if user else "",
                avatar=user.avatar if user and user.avatar else "",
                permissions=pb2.ClubPermission(tokens=permission.tokens),
            )
        )
    return pb2.ClubMembersResponse(
        members=infos,
        total_count=total_count if total_count is not None else len(club.members),
    )
