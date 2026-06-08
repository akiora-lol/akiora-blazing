from pydantic import BaseModel
from typing import Literal
from uuid import UUID
from enum import Enum


class GameStatus(Enum):
    SCHEDULED = "scheduled"
    SIDE_CHOSEN = "side_chosen"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELED = "canceled"


class GameSeriesStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELED = "canceled"


class TournamentStatus(Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELED = "canceled"
