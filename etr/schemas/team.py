"""Team schema file"""
from pydantic import BaseModel, ConfigDict, Field


class TeamSchema(BaseModel):
    """Team pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int = Field(alias="teamId")
    team_name: str = Field(alias="teamName")
    users: list["UserSchema"]
