import grpc
from uuid import UUID

from dishka.integrations.grpcio import FromDishka, inject
from loguru import logger

from game.v1.gameseries_service_pb2 import (
    ToggleReadyRequest,
    DraftActionRequest,
    SetGameWinnerRequest,
    GetSeriesRequest,
    GetSeriesResponse,
    SeriesGame,
)
from game.v1.gameseries_service_pb2_grpc import (
    GameSeriesServiceServicer,
)
from common.types_pb2 import Empty
from common import game_actors_pb2 as actors_pb2

from domain.entities.lol.game_series import GameSeries
from domain.services.lol.game_series_service import GameSeriesService
from domain.services.lol.tournament_serivce import TournamentService
from domain.value_objects.actors import Actor, TeamParticipant
from shared.redis import RedisService


_ACTOR_TYPE_MAP = {1: "user", 2: "team", 3: "club"}
_ACTOR_TYPE_REVERSE = {"user": 1, "team": 2, "club": 3}


def _domain_actor_to_proto(actor: Actor):
    return actors_pb2.Actor(
        id=str(actor.id),
        actor_type=_ACTOR_TYPE_REVERSE.get(actor.type, 0),
    )


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

    @inject
    async def GetSeries(
        self,
        request: GetSeriesRequest,
        context: grpc.aio.ServicerContext,
        game_series_service: FromDishka[GameSeriesService],
    ) -> GetSeriesResponse:
        try:
            series_uuid = UUID(request.series_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Invalid series_id: {request.series_id}",
            )
            return GetSeriesResponse()

        gs = await GameSeries.get(series_uuid)
        if gs is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"GameSeries {request.series_id} not found",
            )
            return GetSeriesResponse()

        # Ordered by creation — this is what the host wants displayed as
        # "Game 1", "Game 2", ... in the BO-N grid.
        games = await game_series_service.game_service.get_by_gs_id(series_uuid)

        proto_games = []
        for g in games:
            winner_actor = None
            if g.results:
                # Game.results stores one TeamParticipant for finished games.
                winner_actor = _domain_actor_to_proto(g.results[0].actor)
            proto_games.append(
                SeriesGame(
                    id=str(g.id),
                    status=g.status.value,
                    winner=winner_actor,
                )
            )

        return GetSeriesResponse(
            id=str(gs.id),
            status=gs.status.value,
            best_of=gs.settings.best_of or 1,
            games=proto_games,
        )

    @inject
    async def SetGameWinner(
        self,
        request: SetGameWinnerRequest,
        context: grpc.aio.ServicerContext,
        tournament_service: FromDishka[TournamentService],
    ) -> Empty:
        try:
            # Resolve tournament_id via the series (single round-trip, avoids
            # making the client pass redundant ids that could disagree).
            gs = await GameSeries.get(UUID(request.series_id))
            if gs is None:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    f"GameSeries {request.series_id} not found",
                )
                return Empty()

            winner_actor = _proto_actor_to_domain(request.winner)
            await tournament_service.set_game_winner(
                tournament_id=gs.tournament_id,
                game_id=UUID(request.game_id),
                actor_id=UUID(request.actor_id),
                winner_actor=winner_actor,
            )
        except PermissionError as e:
            await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except Exception as e:
            logger.exception(
                "SetGameWinner failed series={} game={} actor={}: {}",
                request.series_id,
                request.game_id,
                request.actor_id,
                e,
            )
            await context.abort(
                grpc.StatusCode.FAILED_PRECONDITION, str(e) or type(e).__name__
            )
        return Empty()
