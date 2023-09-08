"""User schema file"""
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """User pydantic schema"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    handler: str
