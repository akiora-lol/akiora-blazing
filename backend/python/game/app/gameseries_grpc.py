import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject

from game.v1.gameseries_service_pb2 import (
    ToggleReadyRequest,
    DraftActionRequest,
)
from game.v1.gameseries_service_pb2_grpc import (
    GameSeriesServiceServicer,
)
from common.types_pb2 import Empty

from domain.services.lol.game_series_service import GameSeriesService
from domain.value_objects.actors import Actor, TeamParticipant
from shared.redis import RedisService


_ACTOR_TYPE_MAP = {1: "user", 2: "team", 3: "club"}


def _proto_actor_to_domain(proto_actor) -> Actor:
    return Actor(
        id=UUID(proto_actor.id),
        type=_ACTOR_TYPE_MAP.get(proto_actor.actor_type, "user"),
    )


class GameSeriesGrpc(GameSeriesServiceServicer):
    @inject
    async def DraftAction(
        self,
        request: DraftActionRequest,
        context: grpc.aio.ServicerContext,
        redis_service: FromDishka[RedisService],
    ) -> Empty:
        command = request.command
        action = command.action
        action_payload = {}
        if action.HasField("pick"):
            action_payload = {"type": "pick", "champion_id": action.pick}
        elif action.HasField("ban"):
            action_payload = {"type": "ban", "champion_id": action.ban}

        await redis_service.publish_pubsub(
            f"draft:{request.series_id}",
            {
                "type": "draft_action",
                "series_id": request.series_id,
                "actor_id": command.actor.id,
                "actor_type": command.actor.actor_type,
                "action": action_payload,
            },
        )
        return Empty()

    @inject
    async def ToggleReady(
        self,
        request: ToggleReadyRequest,
        context: grpc.aio.ServicerContext,
        game_series_service: FromDishka[GameSeriesService],
    ) -> Empty:
        actor = _proto_actor_to_domain(request.actor)
        tp = TeamParticipant(actor=actor, players=[])
        await game_series_service.toggle_ready(UUID(request.series_id), tp)
        return Empty()
