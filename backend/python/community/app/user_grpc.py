import grpc
from uuid import UUID
from loguru import logger

from dishka.integrations.grpcio import inject

from domain.services.user_service import UserService
from domain.entites.user import User, UserType, Social, Birthday, Platform


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
