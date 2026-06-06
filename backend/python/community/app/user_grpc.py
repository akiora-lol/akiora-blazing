import grpc
from uuid import UUID
from loguru import logger

from dishka.integrations.grpcio import inject

from domain.services.user_service import UserService
from domain.entites.user import User, UserType, Social, Birthday, Platform
from domain.entites.friend import Friend


def _paginate(items, pagination):
    page = pagination.page or 1
    page_size = pagination.page_size or 50
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], page, page_size, end < len(items)


def _user_to_proto(user: User, pb2):
    socials = {}
    if user.socials:
        for k, v in user.socials.items():
            socials[k] = pb2.Social(link=v.link, hidden=v.hidden)

    birth_date = None
    if user.birth_date:
        birth_date = pb2.Birthday(
            day=user.birth_date.day.isoformat(),
            hidden=user.birth_date.hidden,
        )

    _type_map = {
        "default": pb2.UserType.DEFAULT,
        "staff": pb2.UserType.STAFF,
        "streamer": pb2.UserType.STREAMER,
        "pro": pb2.UserType.PRO,
        "moderator": pb2.UserType.MODERATOR,
    }
    _gender_map = {
        "male": pb2.Gender.MALE,
        "female": pb2.Gender.FEMALE,
        None: pb2.Gender.GENDER_UNSPECIFIED,
    }

    return pb2.UserResponse(
        id=str(user.id),
        email=user.email,
        nickname=user.nickname,
        user_type=_type_map.get(user.user_type, pb2.UserType.DEFAULT),
        avatar=user.avatar or "",
        bio=user.bio or "",
        gender=_gender_map.get(user.gender, pb2.Gender.GENDER_UNSPECIFIED),
        birth_date=birth_date,
        socials=socials,
        created_at=int(user.created_at.timestamp()),
        last_updated=int(user.last_updated.timestamp()),
    )


def _friend_to_proto(friend: Friend, pb2, status: str | None = None):
    return pb2.FriendResponse(
        id=str(friend.id),
        user_id_1=str(friend.user_id_1),
        user_id_2=str(friend.user_id_2),
        status=status or friend.status,
        created_at=int(friend.created_at.timestamp()),
        updated_at=int(friend.updated_at.timestamp()),
    )


async def _find_friendship(user_id_1: UUID, user_id_2: UUID) -> Friend | None:
    friends = await Friend.find_all().to_list()
    return next(
        (
            friend
            for friend in friends
            if {friend.user_id_1, friend.user_id_2} == {user_id_1, user_id_2}
        ),
        None,
    )


class UserGrpc:
    """Servicer — подставить нужный базовый класс после билда proto."""

    @inject
    async def CreateUser(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        logger.debug("CreateUser email={}", request.email)
        user = await UserService.create(
            email=request.email,
            nickname=request.nickname if request.HasField("nickname") else None,
        )
        return _user_to_proto(user, pb2)

    @inject
    async def GetUser(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        logger.debug("GetUser id={}", request.id)
        user = await UserService.get(UUID(request.id))
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return _user_to_proto(user, pb2)

    @inject
    async def GetUserByEmail(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        logger.debug("GetUserByEmail email={}", request.email)
        user = await UserService.get_by_email(request.email)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return _user_to_proto(user, pb2)

    @inject
    async def UpdateUser(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        logger.debug("UpdateUser id={}", request.user_id)

        _type_reverse = {
            pb2.UserType.DEFAULT: "default",
            pb2.UserType.STAFF: "staff",
            pb2.UserType.STREAMER: "streamer",
            pb2.UserType.PRO: "pro",
            pb2.UserType.MODERATOR: "moderator",
        }
        _gender_reverse = {
            pb2.Gender.MALE: "male",
            pb2.Gender.FEMALE: "female",
        }

        birth_date = None
        if request.HasField("birth_date"):
            from datetime import date
            birth_date = Birthday(
                day=date.fromisoformat(request.birth_date.day),
                hidden=request.birth_date.hidden,
            )

        socials = None
        if request.socials:
            socials = {
                k: Social(link=v.link, hidden=v.hidden)
                for k, v in request.socials.items()
            }

        user = await UserService.update(
            UUID(request.user_id),
            nickname=request.nickname if request.HasField("nickname") else None,
            bio=request.bio if request.HasField("bio") else None,
            avatar=request.avatar if request.HasField("avatar") else None,
            gender=_gender_reverse.get(request.gender),
            user_type=_type_reverse.get(request.user_type),
            birth_date=birth_date,
            socials=socials,
        )
        return _user_to_proto(user, pb2)

    @inject
    async def DeleteUser(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        user = await User.get(UUID(request.user_id))
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        if request.actor_id and UUID(request.actor_id) != user.id:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only user can delete themselves")
        await user.delete()
        return Empty()

    @inject
    async def ListUsers(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        users = await User.find_all().to_list()
        if request.HasField("filter"):
            filter_ = request.filter
            if filter_.search:
                search = filter_.search.lower()
                users = [
                    user for user in users
                    if search in user.nickname.lower()
                    or search in user.email.lower()
                    or (user.bio and search in user.bio.lower())
                ]
            if filter_.user_type:
                type_map = {
                    pb2.UserType.DEFAULT: "default",
                    pb2.UserType.STAFF: "staff",
                    pb2.UserType.STREAMER: "streamer",
                    pb2.UserType.PRO: "pro",
                    pb2.UserType.MODERATOR: "moderator",
                }
                users = [
                    user for user in users
                    if user.user_type == type_map.get(filter_.user_type)
                ]
            if filter_.gender:
                gender_map = {
                    pb2.Gender.MALE: "male",
                    pb2.Gender.FEMALE: "female",
                }
                users = [
                    user for user in users
                    if user.gender == gender_map.get(filter_.gender)
                ]
            if filter_.has_avatar:
                users = [user for user in users if user.avatar]
            if filter_.min_created_at:
                users = [
                    user for user in users
                    if int(user.created_at.timestamp()) >= filter_.min_created_at
                ]
            if filter_.max_created_at:
                users = [
                    user for user in users
                    if int(user.created_at.timestamp()) <= filter_.max_created_at
                ]
        page_items, page, page_size, has_next = _paginate(users, request.pagination)
        return pb2.ListUsersResponse(
            users=[_user_to_proto(user, pb2) for user in page_items],
            total_count=len(users),
            page=page,
            page_size=page_size,
            has_next=has_next,
        )

    @inject
    async def SendFriendRequest(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        sender_id = UUID(request.request.sender_id)
        receiver_id = UUID(request.request.receiver_id)
        if not await User.get(sender_id) or not await User.get(receiver_id):
            await context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        friend = await _find_friendship(sender_id, receiver_id)
        if not friend:
            friend = Friend(
                user_id_1=sender_id,
                user_id_2=receiver_id,
                status="pending",
            )
            await friend.insert()
        return _friend_to_proto(friend, pb2)

    @inject
    async def RespondFriendRequest(self, request, context: grpc.aio.ServicerContext):
        from datetime import UTC, datetime
        from community.user.v1 import user_service_pb2 as pb2
        friend = await Friend.get(UUID(request.response.request_id))
        if not friend:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Friend request not found")
        if UUID(request.response.responder_id) != friend.user_id_2:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only receiver can respond")
        friend.status = "accepted" if request.response.accept else "rejected"
        friend.updated_at = datetime.now(tz=UTC)
        await friend.save()
        return _friend_to_proto(friend, pb2)

    @inject
    async def GetPendingFriendRequests(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        user_id = UUID(request.id)
        friends = [
            friend
            for friend in await Friend.find_all().to_list()
            if friend.user_id_2 == user_id and friend.status == "pending"
        ]
        return pb2.ListFriendsResponse(
            friends=[_friend_to_proto(friend, pb2) for friend in friends],
            total_count=len(friends),
        )

    @inject
    async def GetFriends(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        status_map = {
            1: "accepted",
            2: "pending",
            3: "blocked",
        }
        user_id = UUID(request.user_id)
        status = status_map.get(request.status)
        friends = [
            friend
            for friend in await Friend.find_all().to_list()
            if user_id in {friend.user_id_1, friend.user_id_2}
            and (status is None or friend.status == status)
        ]
        page_items, _, _, _ = _paginate(friends, request.pagination)
        return pb2.ListFriendsResponse(
            friends=[_friend_to_proto(friend, pb2) for friend in page_items],
            total_count=len(friends),
        )

    @inject
    async def RemoveFriend(self, request, context: grpc.aio.ServicerContext):
        from common.types_pb2 import Empty
        friend = await _find_friendship(UUID(request.user_id_1), UUID(request.user_id_2))
        if not friend:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Friendship not found")
        if request.actor_id and UUID(request.actor_id) not in {friend.user_id_1, friend.user_id_2}:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, "Only participants can remove friendship")
        await friend.delete()
        return Empty()

    @inject
    async def BlockUser(self, request, context: grpc.aio.ServicerContext):
        from datetime import UTC, datetime
        from community.user.v1 import user_service_pb2 as pb2
        blocker_id = UUID(request.blocker_id)
        blocked_id = UUID(request.blocked_id)
        friend = await _find_friendship(blocker_id, blocked_id)
        if not friend:
            friend = Friend(user_id_1=blocker_id, user_id_2=blocked_id, status="blocked")
            await friend.insert()
        else:
            friend.user_id_1 = blocker_id
            friend.user_id_2 = blocked_id
            friend.status = "blocked"
            friend.updated_at = datetime.now(tz=UTC)
            await friend.save()
        return _friend_to_proto(friend, pb2)

    @inject
    async def UnblockUser(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        friend = await _find_friendship(UUID(request.blocker_id), UUID(request.blocked_id))
        if not friend:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Block not found")
        await friend.delete()
        return _friend_to_proto(friend, pb2, status="unblocked")

    @inject
    async def GetFriendStatus(self, request, context: grpc.aio.ServicerContext):
        from community.user.v1 import user_service_pb2 as pb2
        friend = await _find_friendship(UUID(request.user_id_1), UUID(request.user_id_2))
        if not friend:
            return pb2.GetFriendStatusResponse(status="none")
        return pb2.GetFriendStatusResponse(
            status=friend.status,
            request_id=str(friend.id),
        )
