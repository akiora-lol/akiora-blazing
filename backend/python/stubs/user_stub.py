import grpc.aio as grpc
from uuid import UUID

from shared.contracts.user import (
    CreateUserRequest,
    GetUserRequest,
    GetUserByEmailRequest,
    UpdateUserRequest,
    UserResponse,
    Gender,
    UserType,
    Birthday,
    Social,
)


import community.user.v1.user_service_pb2 as pb2_module
import community.user.v1.user_service_pb2_grpc as pb2_grpc_module


class UserMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for User service"""

    GENDER_MAP = {
        0: Gender.UNSPECIFIED,
        1: Gender.MALE,
        2: Gender.FEMALE,
    }

    GENDER_TO_PROTO = {
        Gender.UNSPECIFIED: 0,
        Gender.MALE: 1,
        Gender.FEMALE: 2,
    }

    USER_TYPE_MAP = {
        0: UserType.UNSPECIFIED,
        1: UserType.DEFAULT,
        2: UserType.STAFF,
        3: UserType.STREAMER,
        4: UserType.PRO,
        5: UserType.MODERATOR,
    }

    USER_TYPE_TO_PROTO = {
        UserType.UNSPECIFIED: 0,
        UserType.DEFAULT: 1,
        UserType.STAFF: 2,
        UserType.STREAMER: 3,
        UserType.PRO: 4,
        UserType.MODERATOR: 5,
    }

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> UserResponse:
        """Convert gRPC UserResponse to Pydantic UserResponse"""
        socials = {}
        for key, social_pb in grpc_response.socials.items():
            socials[key] = Social(link=social_pb.link, hidden=social_pb.hidden)

        birth_date = None
        if grpc_response.HasField("birth_date"):
            birth_date = Birthday(
                day=grpc_response.birth_date.day,
                hidden=grpc_response.birth_date.hidden,
            )

        return UserResponse(
            id=UUID(grpc_response.id),
            email=grpc_response.email,
            nickname=grpc_response.nickname,
            user_type=cls.USER_TYPE_MAP.get(
                grpc_response.user_type, UserType.UNSPECIFIED
            ),
            avatar=grpc_response.avatar if grpc_response.avatar else None,
            bio=grpc_response.bio if grpc_response.bio else None,
            gender=cls.GENDER_MAP.get(grpc_response.gender, Gender.UNSPECIFIED),
            birth_date=birth_date,
            socials=socials,
            created_at=grpc_response.created_at,
            last_updated=grpc_response.last_updated,
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateUserRequest):
        """Convert Pydantic CreateUserRequest to gRPC CreateUserRequest"""
        return pb2_module.CreateUserRequest(
            email=request.email,
            nickname=request.nickname or "",
        )

    @classmethod
    def to_grpc_get_request(cls, request: GetUserRequest):
        """Convert Pydantic GetUserRequest to gRPC GetUserRequest"""
        return pb2_module.GetUserRequest(id=str(request.id))

    @classmethod
    def to_grpc_get_by_email_request(cls, request: GetUserByEmailRequest):
        """Convert Pydantic GetUserByEmailRequest to gRPC GetUserByEmailRequest"""
        return pb2_module.GetUserByEmailRequest(email=request.email)

    @classmethod
    def to_grpc_update_request(cls, request: UpdateUserRequest):
        """Convert Pydantic UpdateUserRequest to gRPC UpdateUserRequest"""
        grpc_request = pb2_module.UpdateUserRequest(user_id=str(request.user_id))

        if request.nickname is not None:
            grpc_request.nickname = request.nickname
        if request.bio is not None:
            grpc_request.bio = request.bio
        if request.avatar is not None:
            grpc_request.avatar = request.avatar
        if request.gender is not None:
            grpc_request.gender = cls.GENDER_TO_PROTO.get(request.gender, 0)
        if request.user_type is not None:
            grpc_request.user_type = cls.USER_TYPE_TO_PROTO.get(request.user_type, 0)
        if request.birth_date is not None:
            grpc_request.birth_date.CopyFrom(
                pb2_module.Birthday(
                    day=request.birth_date.day,
                    hidden=request.birth_date.hidden,
                )
            )
        if request.socials:
            for key, social in request.socials.items():
                grpc_request.socials[key].link = social.link
                grpc_request.socials[key].hidden = social.hidden

        return grpc_request


class UserStub:
    """Stub for User Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.UserServiceStub(channel)
        self.mapper = UserMapper()

    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateUser(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_user(self, request: GetUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetUser(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_user_by_email(self, request: GetUserByEmailRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_get_by_email_request(request)
        response = await self.stub.GetUserByEmail(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def update_user(self, request: UpdateUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_update_request(request)
        response = await self.stub.UpdateUser(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def create_user_sync(self, request: CreateUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateUser(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_user_sync(self, request: GetUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetUser(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_user_by_email_sync(self, request: GetUserByEmailRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_get_by_email_request(request)
        response = self.stub.GetUserByEmail(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def update_user_sync(self, request: UpdateUserRequest) -> UserResponse:
        grpc_request = self.mapper.to_grpc_update_request(request)
        response = self.stub.UpdateUser(grpc_request)
        return self.mapper.to_pydantic_response(response)
