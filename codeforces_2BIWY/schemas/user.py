"""User schema file"""
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """User pydantic schema"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    handler: str
    email: str | None = None
    vkId: str | None = None
    openId: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    country: str | None = None
    city: str | None = None
    organization: str | None = None
    contribution: int | None = None
    rank: str | None = None
    rating: int | None = None
    maxRank: str | None = None
    maxRating: int | None = None
    lastOnlineTimeSeconds: int | None = None
    registrationTimeSeconds: int | None = None
    friendOfCount: int | None = None
    avatar: str | None = None
    titlePhoto: str | None = None
