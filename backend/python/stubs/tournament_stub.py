import grpc
from uuid import UUID

from shared.contracts.tournament import (
    TournamentResponse,
    ManyTournamentsResponse,
    CreateTournamentRequest,
    GetTournamentRequest,
    ChangeBracketRequest,
    AddParticipantRequest,
    AddTeamParticipantRequest,
    RemoveParticipantRequest,
    TournamentSettings,
    LolTournamentSettings,
    TftTournamentSettings,
    ValorantTournamentSettings,
    Actor,
    TeamParticipant,
    ActorType,
    GameType,
    LolGameMode,
    LolBracketMode,
    Status,
    TournamentType,
)

import game.v1.tournament_service_pb2 as pb2_module
import game.v1.tournament_service_pb2_grpc as pb2_grpc_module
import common.game_actors_pb2 as actors_pb2_module


class TournamentMapper:
    """Mapper between gRPC protobuf messages and Pydantic models for Tournament service"""

    ACTOR_TYPE_MAP = {
        0: ActorType.ACTOR_UNSPECIFIED,
        1: ActorType.USER,
        2: ActorType.TEAM,
        3: ActorType.CLUB,
    }

    ACTOR_TYPE_TO_PROTO = {v: k for k, v in ACTOR_TYPE_MAP.items()}

    GAME_TYPE_MAP = {
        0: GameType.GAME_TYPE_UNSPECIFIED,
        1: GameType.LOL,
        2: GameType.TFT,
        3: GameType.VALORANT,
    }

    GAME_TYPE_TO_PROTO = {v: k for k, v in GAME_TYPE_MAP.items()}

    STATUS_MAP = {
        0: Status.STATUS_UNSPECIFIED,
        1: Status.SCHEDULED,
        2: Status.ACTIVE,
        3: Status.FINISHED,
        4: Status.CANCELLED,
    }

    TOURNAMENT_TYPE_MAP = {
        0: TournamentType.UNSPECIFIED,
        1: TournamentType.PRESIGN,
        2: TournamentType.PICKEM,
    }

    TOURNAMENT_TYPE_TO_PROTO = {v: k for k, v in TOURNAMENT_TYPE_MAP.items()}

    LOL_BRACKET_MODE_MAP = {
        0: LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED,
        1: LolBracketMode.DOUBLE_ELIM,
        2: LolBracketMode.SINGLE_ELIM_THIRD_PLACE,
        3: LolBracketMode.SINGLE_ELIM_NO_THIRD_PLACE,
        4: LolBracketMode.SWISS,
        5: LolBracketMode.ROUND_ROBIN,
        6: LolBracketMode.SCRIM,
    }

    LOL_BRACKET_MODE_TO_PROTO = {v: k for k, v in LOL_BRACKET_MODE_MAP.items()}

    LOL_GAME_MODE_MAP = {
        0: LolGameMode.GAME_MODE_UNSPECIFIED,
        1: LolGameMode.CLASSIC,
        2: LolGameMode.FEARLESS,
        3: LolGameMode.IRON_MAN,
        4: LolGameMode.ALL_RANDOM,
    }

    LOL_GAME_MODE_TO_PROTO = {v: k for k, v in LOL_GAME_MODE_MAP.items()}

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
    def _to_pydantic_settings(cls, grpc_settings) -> TournamentSettings:
        lol = None
        if grpc_settings.HasField("lol"):
            lol = LolTournamentSettings(
                tournament_type=cls.TOURNAMENT_TYPE_MAP.get(
                    grpc_settings.lol.tournament_type, TournamentType.UNSPECIFIED
                ),
                bracket_mode=cls.LOL_BRACKET_MODE_MAP.get(
                    grpc_settings.lol.bracket_mode,
                    LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED,
                ),
                draft_mode=[
                    cls.LOL_GAME_MODE_MAP.get(m, LolGameMode.GAME_MODE_UNSPECIFIED)
                    for m in grpc_settings.lol.draft_mode
                ],
                team_size=grpc_settings.lol.team_size,
                map=grpc_settings.lol.map,
                forbidden_champions=list(grpc_settings.lol.forbidden_champions),
                series_best_of=list(grpc_settings.lol.series_best_of),
            )

        tft = None
        if grpc_settings.HasField("tft"):
            tft = TftTournamentSettings(todo=grpc_settings.tft.todo or None)

        valorant = None
        if grpc_settings.HasField("valorant"):
            valorant = ValorantTournamentSettings(
                todo=grpc_settings.valorant.todo or None
            )

        return TournamentSettings(
            game_type=cls.GAME_TYPE_MAP.get(
                grpc_settings.game_type, GameType.GAME_TYPE_UNSPECIFIED
            ),
            lol=lol,
            tft=tft,
            valorant=valorant,
        )

    @classmethod
    def to_pydantic_response(cls, grpc_response) -> TournamentResponse:
        participants = [cls._to_pydantic_actor(p) for p in grpc_response.participants]

        return TournamentResponse(
            id=UUID(grpc_response.id),
            host=cls._to_pydantic_actor(grpc_response.host),
            participants=participants,
            settings=cls._to_pydantic_settings(grpc_response.settings),
            game_series_ids=list(grpc_response.game_series_ids),
            start=grpc_response.start,
            end=grpc_response.end if grpc_response.end else None,
            status=cls.STATUS_MAP.get(grpc_response.status, Status.STATUS_UNSPECIFIED),
            prizepool=grpc_response.prizepool if grpc_response.prizepool else None,
        )

    @classmethod
    def to_grpc_create_request(cls, request: CreateTournamentRequest):
        grpc_request = pb2_module.CreateTournamentRequest(
            host=cls._to_grpc_actor(request.host),
            start=request.start,
            is_open=request.is_open,
        )
        if request.prizepool:
            grpc_request.prizepool = request.prizepool
        return grpc_request

    @classmethod
    def to_grpc_get_request(cls, request: GetTournamentRequest):
        grpc_request = pb2_module.GetTournamentRequest(ids=request.ids)
        if request.game_type:
            grpc_request.game_type = cls.GAME_TYPE_TO_PROTO.get(request.game_type, 0)
        return grpc_request


class TournamentStub:
    """Stub for Tournament Service gRPC calls with pydantic mapping"""

    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.stub = pb2_grpc_module.TournamentServiceStub(channel)
        self.mapper = TournamentMapper()

    async def create_tournament(
        self, request: CreateTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = await self.stub.CreateTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    async def get_tournament(
        self, request: GetTournamentRequest
    ) -> ManyTournamentsResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = await self.stub.GetTournament(grpc_request)
        tournaments = [
            self.mapper.to_pydantic_response(t) for t in response.tournaments
        ]
        return ManyTournamentsResponse(tournaments=tournaments)

    def create_tournament_sync(
        self, request: CreateTournamentRequest
    ) -> TournamentResponse:
        grpc_request = self.mapper.to_grpc_create_request(request)
        response = self.stub.CreateTournament(grpc_request)
        return self.mapper.to_pydantic_response(response)

    def get_tournament_sync(
        self, request: GetTournamentRequest
    ) -> ManyTournamentsResponse:
        grpc_request = self.mapper.to_grpc_get_request(request)
        response = self.stub.GetTournament(grpc_request)
        tournaments = [
            self.mapper.to_pydantic_response(t) for t in response.tournaments
        ]
        return ManyTournamentsResponse(tournaments=tournaments)
