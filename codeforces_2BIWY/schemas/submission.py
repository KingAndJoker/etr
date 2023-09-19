"""Submission schema file"""
from pydantic import BaseModel, ConfigDict

from codeforces_2BIWY.schemas.problem import ProblemSchema
from codeforces_2BIWY.schemas.user import UserSchema
from codeforces_2BIWY.schemas.team import TeamSchema


class SubmissionSchema(BaseModel):
    """
    Submission pydantic schema
    https://codeforces.com/apiHelp/objects#Submission
    """

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    contestId: int | None = None
    creationTimeSeconds: int | None = None
    relativeTimeSeconds: int | None = None
    problem: ProblemSchema | None = None
    author: UserSchema | TeamSchema | None = None
    programmingLanguage: str | None = None
    verdict: str | None = None
    passedTestCount: int | None = None
    timeConsumedMillis: int | None = None
    memoryConsumedBytes: int | None = None
    points: int | None = None
