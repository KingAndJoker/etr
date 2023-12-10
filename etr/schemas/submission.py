"""Submission schema file"""
from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from etr.schemas.problem import ProblemSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema


class SubmissionSchema(BaseModel):
    """
    Submission pydantic schema
    https://codeforces.com/apiHelp/objects#Submission
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    contest_id: int | None = None
    creation_time_seconds: int | None = None
    relative_time_seconds: int | None = None
    problem: ProblemSchema | None = None
    author: UserSchema | TeamSchema | None = None
    programming_language: str | None = None
    verdict: str | None = None
    testset: str | None = None
    passed_test_count: int | None = None
    time_consumed_millis: int | None = None
    memory_consumed_bytes: int | None = None
    points: int | None = None
    type_of_member: str | None = None
