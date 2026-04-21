from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class ActorType(str, Enum):
    ACTOR_UNSPECIFIED = "ACTOR_UNSPECIFIED"
    USER = "USER"
    TEAM = "TEAM"
    CLUB = "CLUB"


class GameType(str, Enum):
    GAME_TYPE_UNSPECIFIED = "GAME_TYPE_UNSPECIFIED"
    LOL = "LOL"
    TFT = "TFT"
    VALORANT = "VALORANT"


class LolGameMode(str, Enum):
    GAME_MODE_UNSPECIFIED = "GAME_MODE_UNSPECIFIED"
    CLASSIC = "CLASSIC"
    FEARLESS = "FEARLESS"
    IRON_MAN = "IRON_MAN"
    ALL_RANDOM = "ALL_RANDOM"


class LolBracketMode(str, Enum):
    LOL_BRACKET_MODE_UNSPECIFIED = "LOL_BRACKET_MODE_UNSPECIFIED"
    DOUBLE_ELIM = "DOUBLE_ELIM"
    SINGLE_ELIM_THIRD_PLACE = "SINGLE_ELIM_THIRD_PLACE"
    SINGLE_ELIM_NO_THIRD_PLACE = "SINGLE_ELIM_NO_THIRD_PLACE"
    SWISS = "SWISS"
    ROUND_ROBIN = "ROUND_ROBIN"
    SCRIM = "SCRIM"


class Status(str, Enum):
    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"


class TournamentType(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    PRESIGN = "PRESIGN"
    PICKEM = "PICKEM"


class Actor(BaseModel):
    id: UUID
    actor_type: ActorType


class TeamParticipant(BaseModel):
    participant: Actor
    user_ids: List[str] = Field(default_factory=list)


class LolGameSettings(BaseModel):
    mode: LolGameMode = LolGameMode.GAME_MODE_UNSPECIFIED
    team_size: int = 5
    map: int = 11
    best_of: int = 1


class TftGameSettings(BaseModel):
    todo: Optional[str] = None


class ValorantGameSettings(BaseModel):
    todo: Optional[str] = None


class GameSettings(BaseModel):
    game_type: GameType = GameType.GAME_TYPE_UNSPECIFIED
    lol: Optional[LolGameSettings] = None
    tft: Optional[TftGameSettings] = None
    valorant: Optional[ValorantGameSettings] = None


class LolTournamentSettings(BaseModel):
    tournament_type: TournamentType = TournamentType.UNSPECIFIED
    bracket_mode: LolBracketMode = LolBracketMode.LOL_BRACKET_MODE_UNSPECIFIED
    draft_mode: List[LolGameMode] = Field(default_factory=list)
    team_size: int = 5
    map: int = 11
    forbidden_champions: List[int] = Field(default_factory=list)
    series_best_of: List[int] = Field(default_factory=list)


class TftTournamentSettings(BaseModel):
    todo: Optional[str] = None


class ValorantTournamentSettings(BaseModel):
    todo: Optional[str] = None


class TournamentSettings(BaseModel):
    game_type: GameType = GameType.GAME_TYPE_UNSPECIFIED
    lol: Optional[LolTournamentSettings] = None
    tft: Optional[TftTournamentSettings] = None
    valorant: Optional[ValorantTournamentSettings] = None


class TournamentResponse(BaseModel):
    id: UUID
    host: Actor
    participants: List[Actor] = Field(default_factory=list)
    settings: TournamentSettings
    game_series_ids: List[str] = Field(default_factory=list)
    start: int
    end: Optional[int] = None
    status: Status = Status.STATUS_UNSPECIFIED
    prizepool: Optional[str] = None

    class Config:
        from_attributes = True


class ManyTournamentsResponse(BaseModel):
    tournaments: List[TournamentResponse] = Field(default_factory=list)


class CreateTournamentRequest(BaseModel):
    host: Actor
    settings: TournamentSettings
    start: int
    prizepool: Optional[str] = None
    is_open: bool = False


class GetTournamentRequest(BaseModel):
    ids: List[str] = Field(default_factory=list)
    game_type: Optional[GameType] = None


class ChangeBracketRequest(BaseModel):
    tournament_id: UUID
    swap_initiator: Actor
    swap_victim: Actor


class AddParticipantRequest(BaseModel):
    tournament_id: UUID
    participant: Actor


class AddTeamParticipantRequest(BaseModel):
    tournament_id: UUID
    team_participant: TeamParticipant


class RemoveParticipantRequest(BaseModel):
    tournament_id: UUID
    participant_id: str
