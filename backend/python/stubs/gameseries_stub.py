import grpc
from uuid import UUID

from shared.contracts.gameseries import (
    ToggleReadyRequest,
    GameSeriesResponse,
)
from shared.contracts.tournament import Actor, ActorType, GameType, GameSettings

import game.v1.gameseries_service_pb2 as pb2_module
import game.v1.gameseries_service_pb2_grpc as pb2_grpc_module
import common.game_actors_pb2 as actors_pb2_module


class GameSeriesMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for GameSeries service"""

    ACTOR_TYPE_MAP = {
        0: ActorType.ACTOR_UNSPECIFIED,
        1: ActorType.USER,
        2: ActorType.TEAM,
        3: ActorType.CLUB,
    }

    ACTOR_TYPE_TO_PROTO = {v: k for k, v in ACTOR_TYPE_MAP.items()}

    @classmethod
    def _to_pydantic_actor(cls, grpc_actor) -> Actor:
        return Actor(
            id=UUID(grpc_actor.id),
            actor_type=cls.ACTOR_TYPE_MAP.get(
                grpc_actor.actor_type, ActorType.ACTOR_UNSPECIFIED
            ),
        )

    @classmethod
    def _to_grpc_actor(cls, actor: Actor):
        return actors_pb2_module.Actor(
            id=str(actor.id),
            actor_type=cls.ACTOR_TYPE_TO_PROTO.get(actor.actor_type, 0),
        )

    @classmethod
    def to_grpc_toggle_ready_request(cls, request: ToggleReadyRequest):
        return pb2_module.ToggleReadyRequest(
            series_id=str(request.series_id),
            actor=cls._to_grpc_actor(request.actor),
        )


class GameSeriesStub:
    """Stub for GameSeries Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.GameSeriesServiceStub(channel)
        self.mapper = GameSeriesMapper()

    async def toggle_ready(self, request: ToggleReadyRequest):
        grpc_request = self.mapper.to_grpc_toggle_ready_request(request)
        return await self.stub.ToggleReady(grpc_request)

    def toggle_ready_sync(self, request: ToggleReadyRequest):
        grpc_request = self.mapper.to_grpc_toggle_ready_request(request)
        return self.stub.ToggleReady(grpc_request)
