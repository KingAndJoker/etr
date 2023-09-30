"""Submission schema file"""
from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from codeforces_2BIWY.schemas.problem import ProblemSchema
from codeforces_2BIWY.schemas.user import UserSchema
from codeforces_2BIWY.schemas.team import TeamSchema


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
    contest_id: int | None = Field(default=None, alias="contestId")
    creation_time_seconds: int | None = Field(
        default=True,
        alias="creationTimeSeconds"
    )
    relative_time_seconds: int | None = Field(
        default=None,
        alias="relativeTimeSeconds"
    )
    problem: ProblemSchema | None = None
    author: UserSchema | TeamSchema | None = None
    programming_language: str | None = Field(
        default=None,
        alias="programmingLanguage"
    )
    verdict: str | None = None
    testset: str | None = None
    passed_test_count: int | None = Field(
        default=None,
        alias="passedTestCount"
    )
    time_consumed_millis: int | None = Field(
        default=None,
        alias="timeConsumedMillis"
    )
    memory_consumed_bytes: int | None = Field(
        default=None,
        alias="memoryConsumedBytes"
    )
    points: int | None = None
