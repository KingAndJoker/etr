"""User schema file"""
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """User pydantic schema"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    handler: str
    email: str = None
    vkId: str = None
    openId: str = None
    firstName: str = None
    lastName: str = None
    country: str = None
    city: str = None
    organization: str = None
    contribution: int = None
    rank: str = None
    rating: int = None
    maxRank: str = None
    maxRating: int = None
    lastOnlineTimeSeconds: int = None
    registrationTimeSeconds: int = None
    friendOfCount: int = None
    avatar: str = None
    titlePhoto: str = None
