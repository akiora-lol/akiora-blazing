from beanie import Document, Indexed
from pydantic import ConfigDict, Field, EmailStr, field_serializer, BaseModel
from uuid import UUID, uuid4
from typing import Literal, Annotated
from datetime import datetime, UTC, date
import pymongo


def time_now():
    return datetime.now(tz=UTC)


def default_name():
    return f"user{int(time_now().timestamp())}"


UserType = Literal["default", "staff", "streamer", "pro", "moderator"]

Platform = Literal["vk", "tg", "ds", "yt", "tw", "sc"]


class Social(BaseModel):
    link: str
    hidden: bool = Field(default=True)


class Birthday(BaseModel):
    day: date
    hidden: bool = Field(default=True)


class LeagueAccount(BaseModel):
    status: Literal["done", "pending"] = "pending"
    username: str
    tagline: str
    server: str
    profile_image_url: str | None = None
    solo_tier: str | None = None
    solo_division: int | None = None
    solo_lp: int | None = None
    solo_tier_image_url: str | None = None


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    email: Annotated[EmailStr, Indexed(unique=True)]
    user_type: UserType = "default"
    avatar: str | None = None
    bio: str | None = Field(default=None, max_length=500)
    nickname: Annotated[str, Indexed(unique=True)] = Field(default_factory=default_name)
    gender: Literal["male", "female"] | None = None
    birth_date: Birthday | None = None
    socials: dict[Platform, Social] | None = None
    league_accounts: list[LeagueAccount] | None = None
    created_at: datetime = Field(default_factory=time_now)
    last_updated: datetime = Field(default_factory=time_now)

    @field_serializer("id")
    def serialize_id(self, id: UUID):
        return str(id)

    @field_serializer("created_at")
    def serialize_ca(self, dt: datetime):
        return dt.isoformat()

    @field_serializer("last_updated")
    def serialize_la(self, dt: datetime):
        return dt.isoformat()

    model_config = ConfigDict(extra="ignore")

    class Settings:
        bson_encoders = {UUID: str}
