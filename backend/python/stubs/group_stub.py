import grpc
from uuid import UUID

from shared.contracts.group import (
    GroupResponse,
    CreateGroupRequest,
    GetGroupRequest,
    PatchGroupRequest,
)

import community.group.v1.group_service_pb2 as pb2_module
import community.group.v1.group_service_pb2_grpc as pb2_grpc_module


class GroupMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Group service"""

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> GroupResponse:
        return GroupResponse(
            id=UUID(grpc_response.id),
            owner_id=UUID(grpc_response.owner_id),
            name=grpc_response.name,
            users=list(grpc_response.users),
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateGroupRequest):
        return pb2_module.CreateGroupRequest(
            owner_id=str(request.owner_id),
            name=request.name,
        )

    @classmethod
    def to_grpc_get_request(cls, request: GetGroupRequest):
        return pb2_module.GetGroupRequest(id=str(request.id))

    @classmethod
    def to_grpc_patch_request(cls, request: PatchGroupRequest):
        grpc_request = pb2_module.PatchGroupRequest(
            owner_id=str(request.owner_id),
        )
        if request.name:
            grpc_request.name = request.name
        grpc_request.add_users.extend(request.add_users)
        grpc_request.delete_users.extend(request.delete_users)
        return grpc_request


class GroupStub:
    """Stub for Group Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.GroupServiceStub(channel)
        self.mapper = GroupMapper()

    async def create_group(self, request: CreateGroupRequest) -> GroupResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateGroup(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_group(self, request: GetGroupRequest) -> GroupResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetGroup(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def patch_group(self, request: PatchGroupRequest) -> GroupResponse:
        grpc_request = self.mapper.to_grpc_patch_request(request)
        response = await self.stub.PatchGroup(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def create_group_sync(self, request: CreateGroupRequest) -> GroupResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateGroup(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_group_sync(self, request: GetGroupRequest) -> GroupResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetGroup(grpc_request)
        return self.mapper.to_pydantic_response(response)
