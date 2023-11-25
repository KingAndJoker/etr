"""Codeforces Team schema file"""
from pydantic import BaseModel, ConfigDict, validator, Field

from etr.library.codeforces.schemas.user import CodeforcesUserSchema


class CodeforcesTeamSchema(BaseModel):
    """Codeforces Team pydantic schema"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    teamId: int
    teamName: str
    users: list[CodeforcesUserSchema] = Field(alias="members")

    @validator("users", pre=True)
    def validate_users(
        data: dict | list[CodeforcesUserSchema]
    ) -> list[CodeforcesUserSchema]:
        if isinstance(data, list) and all(isinstance(user, CodeforcesUserSchema) for user in data):
            return data

        users = []
        for user_data in data:
            user = CodeforcesUserSchema(**user_data)
            users.append(user)
        return users
