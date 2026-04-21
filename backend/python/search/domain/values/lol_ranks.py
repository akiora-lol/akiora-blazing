from enum import Enum
from pydantic import BaseModel, Field, model_validator
from .servers import Server


class LolRankName(Enum):
    IRON = "iron"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    EMERALD = "emerald"
    DIAMOND = "diamond"
    MASTER = "master"
    GRANDMASTER = "grandmaster"
    CHALLENGER = "challenger"


class LeagueRank(BaseModel):
    rank: LolRankName
    division: int = Field(1, ge=1, le=4)
    lp: int | None = Field(None, ge=0)

    @model_validator(mode="after")
    def fix(self):
        if self.rank in [
            LolRankName.MASTER,
            LolRankName.GRANDMASTER,
            LolRankName.CHALLENGER,
        ]:
            self.division = 1
        return self


class RankRange(BaseModel):
    server: Server
    min_rank: LeagueRank
    max_rank: LeagueRank
