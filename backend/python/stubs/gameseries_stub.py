import grpc
from uuid import UUID

from shared.contracts.gameseries import (
    DraftActionRequest,
    ToggleReadyRequest,
    SetGameWinnerRequest,
    GameSeriesResponse,
    GetSeriesResponse,
    SeriesGameView,
)
from shared.contracts.tournament import Actor, ActorType, GameType, GameSettings

import game.v1.gameseries_service_pb2 as pb2_module
import game.v1.gameseries_service_pb2_grpc as pb2_grpc_module
import common.game_actors_pb2 as actors_pb2_module
import common.game_draft_pb2 as draft_pb2_module


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

    @classmethod
    def to_grpc_set_game_winner_request(cls, request: SetGameWinnerRequest):
        return pb2_module.SetGameWinnerRequest(
            series_id=str(request.series_id),
            game_id=str(request.game_id),
            actor_id=str(request.actor_id),
            winner=cls._to_grpc_actor(request.winner),
        )

    @classmethod
    def from_grpc_get_series_response(cls, response) -> GetSeriesResponse:
        return GetSeriesResponse(
            id=UUID(response.id),
            status=response.status,
            best_of=response.best_of or 1,
            games=[
                SeriesGameView(
                    id=UUID(g.id),
                    status=g.status,
                    # winner is a default-constructed Actor when unset
                    # (proto3 has no presence for messages in py-stubs of
                    # this style); treat empty actor id as "no winner".
                    winner=cls._to_pydantic_actor(g.winner) if g.winner.id else None,
                )
                for g in response.games
            ],
        )

    @classmethod
    def to_grpc_draft_action_request(cls, request: DraftActionRequest):
        action = draft_pb2_module.Action()
        if request.command.action.pick is not None:
            action.pick = request.command.action.pick
        if request.command.action.ban is not None:
            action.ban = request.command.action.ban
        return pb2_module.DraftActionRequest(
            series_id=str(request.series_id),
            command=draft_pb2_module.Command(
                actor=cls._to_grpc_actor(request.command.actor),
                action=action,
            ),
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

    async def draft_action(self, request: DraftActionRequest):
        grpc_request = self.mapper.to_grpc_draft_action_request(request)
        return await self.stub.DraftAction(grpc_request)

    async def set_game_winner(self, request: SetGameWinnerRequest):
        grpc_request = self.mapper.to_grpc_set_game_winner_request(request)
        return await self.stub.SetGameWinner(grpc_request)

    async def get_series(self, series_id: UUID) -> GetSeriesResponse:
        grpc_request = pb2_module.GetSeriesRequest(series_id=str(series_id))
        response = await self.stub.GetSeries(grpc_request)
        return self.mapper.from_grpc_get_series_response(response)

    def toggle_ready_sync(self, request: ToggleReadyRequest):
        grpc_request = self.mapper.to_grpc_toggle_ready_request(request)
        return self.stub.ToggleReady(grpc_request)
