"""Codeforces Team schema file"""
from pydantic import BaseModel, ConfigDict


class CodeforcesTeamSchema(BaseModel):
    """Codeforces Team pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    teamId: int
    teamName: str
    users: list["CodeforcesUserSchema"]
