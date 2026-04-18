import grpc
from uuid import UUID

from dishka.integrations.grpcio import inject

from domain.services.club_service import ClubService
from domain.entites.club import Club, ClubPermission


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
        fields = [list(fg.fields) for fg in request.fields]
        club = await ClubService.create(
            owner_id=UUID(request.owner_id),
            name=request.name,
            fields=fields,
        )
        return _club_to_proto(club, pb2)

    @inject
    async def GetClub(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
        club = await ClubService.get(UUID(request.club_id))
        if not club:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Club not found")
        return _club_to_proto(club, pb2)

    @inject
    async def UpdateClub(self, request, context: grpc.aio.ServicerContext):
        from community.club.v1 import club_service_pb2 as pb2
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
        club = await ClubService.add_member(
            club_id=UUID(request.club_id),
            user_id=UUID(request.user_id),
            tokens=list(request.tokens) or None,
        )
        return _club_to_proto(club, pb2)

    @inject
    async def RemoveMember(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        await ClubService.remove_member(
            club_id=UUID(request.club_id),
            user_id=UUID(request.user_id),
        )
        return Empty()

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
