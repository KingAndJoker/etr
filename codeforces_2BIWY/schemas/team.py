"""Team schema file"""
from pydantic import BaseModel, ConfigDict


class TeamSchema(BaseModel):
    """Team pydantic schema"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    teamName: str
    users: list["UserSchema"]
