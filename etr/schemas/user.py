"""User schema file"""
from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    """User pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int | None = None
    handle: str
    email: str | None = None
    vk_id: str | None = Field(default=None, alias="vkId")
    open_id: str | None = Field(default=None, alias="openId")
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    country: str | None = None
    city: str | None = None
    organization: str | None = None
    contribution: int | None = None
    rank: str | None = None
    rating: int | None = None
    max_rank: str | None = Field(default=None, alias="maxRank")
    max_rating: int | None = Field(default=None, alias="maxRating")
    last_online_time_seconds: int | None = Field(
        default=None,
        alias="lastOnlineTimeSeconds"
    )
    registration_time_seconds: int | None = Field(
        default=None,
        alias="registrationTimeSeconds"
    )
    friend_of_count: int | None = Field(default=None, alias="friendOfCount")
    avatar: str | None = None
    title_photo: str | None = Field(default=None, alias="titlePhoto")
