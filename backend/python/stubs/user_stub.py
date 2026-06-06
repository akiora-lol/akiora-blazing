import grpc.aio as grpc
from uuid import UUID

from shared.contracts.user import (
    BlockUserRequest,
    CreateUserRequest,
    DeleteUserRequest,
    FriendResponse,
    GetUserRequest,
    GetUserByEmailRequest,
    GetFriendStatusRequest,
    GetFriendStatusResponse,
    ListFriendsRequest,
    ListFriendsResponse,
    ListUsersRequest,
    ListUsersResponse,
    RemoveFriendRequest,
    RespondFriendRequestRequest,
    SendFriendRequestRequest,
    UnblockUserRequest,
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

    FRIEND_STATUS_TO_PROTO = {
        "UNSPECIFIED": 0,
        "FRIEND_STATUS_UNSPECIFIED": 0,
        "ACCEPTED": 1,
        "PENDING": 2,
        "BLOCKED": 3,
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
    def to_pydantic_list_response(cls, grpc_response) -> ListUsersResponse:
        return ListUsersResponse(
            users=[cls.to_pydantic_response(user) for user in grpc_response.users],
            total_count=grpc_response.total_count,
            page=grpc_response.page,
            page_size=grpc_response.page_size,
            has_next=grpc_response.has_next,
        )

    @classmethod
    def to_pydantic_friend_response(cls, grpc_response) -> FriendResponse:
        return FriendResponse(
            id=UUID(grpc_response.id),
            user_id_1=UUID(grpc_response.user_id_1),
            user_id_2=UUID(grpc_response.user_id_2),
            status=grpc_response.status,
            created_at=grpc_response.created_at,
            updated_at=grpc_response.updated_at,
        )

    @classmethod
    def to_pydantic_friends_response(cls, grpc_response) -> ListFriendsResponse:
        return ListFriendsResponse(
            friends=[
                cls.to_pydantic_friend_response(friend)
                for friend in grpc_response.friends
            ],
            total_count=grpc_response.total_count,
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

    @classmethod
    def to_grpc_pagination(cls, pagination):
        return pb2_module.PaginationRequest(
            page=pagination.page,
            page_size=pagination.page_size,
            before_timestamp=pagination.before_timestamp or 0,
        )

    @classmethod
    def to_grpc_list_request(cls, request: ListUsersRequest):
        grpc_filter = pb2_module.UserFilter(has_avatar=request.filter.has_avatar)
        if request.filter.search:
            grpc_filter.search = request.filter.search
        if request.filter.user_type:
            grpc_filter.user_type = cls.USER_TYPE_TO_PROTO.get(request.filter.user_type, 0)
        if request.filter.gender:
            grpc_filter.gender = cls.GENDER_TO_PROTO.get(request.filter.gender, 0)
        if request.filter.min_created_at:
            grpc_filter.min_created_at = request.filter.min_created_at
        if request.filter.max_created_at:
            grpc_filter.max_created_at = request.filter.max_created_at
        return pb2_module.ListUsersRequest(
            filter=grpc_filter,
            pagination=cls.to_grpc_pagination(request.pagination),
        )

    @classmethod
    def to_grpc_delete_request(cls, request: DeleteUserRequest):
        return pb2_module.DeleteUserRequest(
            user_id=str(request.user_id),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_send_friend_request(cls, request: SendFriendRequestRequest):
        return pb2_module.SendFriendRequestRequest(
            request=pb2_module.FriendRequest(
                sender_id=str(request.request.sender_id),
                receiver_id=str(request.request.receiver_id),
            )
        )

    @classmethod
    def to_grpc_respond_friend_request(cls, request: RespondFriendRequestRequest):
        return pb2_module.RespondFriendRequestRequest(
            response=pb2_module.RespondFriendRequest(
                request_id=str(request.response.request_id),
                responder_id=str(request.response.responder_id),
                accept=request.response.accept,
            )
        )

    @classmethod
    def to_grpc_list_friends_request(cls, request: ListFriendsRequest):
        return pb2_module.ListFriendsRequest(
            user_id=str(request.user_id),
            pagination=cls.to_grpc_pagination(request.pagination),
            status=cls.FRIEND_STATUS_TO_PROTO.get(request.status, 0),
        )

    @classmethod
    def to_grpc_remove_friend_request(cls, request: RemoveFriendRequest):
        return pb2_module.RemoveFriendRequest(
            user_id_1=str(request.user_id_1),
            user_id_2=str(request.user_id_2),
            actor_id=str(request.actor_id),
        )

    @classmethod
    def to_grpc_block_user_request(cls, request: BlockUserRequest):
        return pb2_module.BlockUserRequest(
            blocker_id=str(request.blocker_id),
            blocked_id=str(request.blocked_id),
        )

    @classmethod
    def to_grpc_unblock_user_request(cls, request: UnblockUserRequest):
        return pb2_module.UnblockUserRequest(
            blocker_id=str(request.blocker_id),
            blocked_id=str(request.blocked_id),
        )

    @classmethod
    def to_grpc_friend_status_request(cls, request: GetFriendStatusRequest):
        return pb2_module.GetFriendStatusRequest(
            user_id_1=str(request.user_id_1),
            user_id_2=str(request.user_id_2),
        )


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

    async def delete_user(self, request: DeleteUserRequest):
        grpc_request = self.mapper.to_grpc_delete_request(request)
        return await self.stub.DeleteUser(grpc_request)

    async def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        grpc_request = self.mapper.to_grpc_list_request(request)
        response = await self.stub.ListUsers(grpc_request)
        return self.mapper.to_pydantic_list_response(response)

    async def send_friend_request(
        self, request: SendFriendRequestRequest
    ) -> FriendResponse:
        grpc_request = self.mapper.to_grpc_send_friend_request(request)
        response = await self.stub.SendFriendRequest(grpc_request)
        return self.mapper.to_pydantic_friend_response(response)

    async def respond_friend_request(
        self, request: RespondFriendRequestRequest
    ) -> FriendResponse:
        grpc_request = self.mapper.to_grpc_respond_friend_request(request)
        response = await self.stub.RespondFriendRequest(grpc_request)
        return self.mapper.to_pydantic_friend_response(response)

    async def get_pending_friend_requests(
        self, request: GetUserRequest
    ) -> ListFriendsResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetPendingFriendRequests(grpc_request)
        return self.mapper.to_pydantic_friends_response(response)

    async def get_friends(self, request: ListFriendsRequest) -> ListFriendsResponse:
        grpc_request = self.mapper.to_grpc_list_friends_request(request)
        response = await self.stub.GetFriends(grpc_request)
        return self.mapper.to_pydantic_friends_response(response)

    async def remove_friend(self, request: RemoveFriendRequest):
        grpc_request = self.mapper.to_grpc_remove_friend_request(request)
        return await self.stub.RemoveFriend(grpc_request)

    async def block_user(self, request: BlockUserRequest) -> FriendResponse:
        grpc_request = self.mapper.to_grpc_block_user_request(request)
        response = await self.stub.BlockUser(grpc_request)
        return self.mapper.to_pydantic_friend_response(response)

    async def unblock_user(self, request: UnblockUserRequest) -> FriendResponse:
        grpc_request = self.mapper.to_grpc_unblock_user_request(request)
        response = await self.stub.UnblockUser(grpc_request)
        return self.mapper.to_pydantic_friend_response(response)

    async def get_friend_status(
        self, request: GetFriendStatusRequest
    ) -> GetFriendStatusResponse:
        grpc_request = self.mapper.to_grpc_friend_status_request(request)
        response = await self.stub.GetFriendStatus(grpc_request)
        return GetFriendStatusResponse(
            status=response.status,
            request_id=UUID(response.request_id) if response.request_id else None,
        )

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
