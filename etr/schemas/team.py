"""Team schema file"""
from pydantic import BaseModel, ConfigDict, Field


class TeamSchema(BaseModel):
    """Team pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    team_name: str
    users: list["UserSchema"]
