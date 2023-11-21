"""Codeforces Submission schema file"""
from pydantic import (
    BaseModel,
    ConfigDict
)

from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.library.codeforces.schemas.user import CodeforcesUserSchema


class CodeforcesSubmissionSchema(BaseModel):
    """
    Submission pydantic schema
    https://codeforces.com/apiHelp/objects#Submission
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    contestId: int | None = None
    creationTimeSeconds: int | None = None
    relativeTimeSeconds: int | None = None
    problem: CodeforcesProblemSchema | None = None
    author: CodeforcesUserSchema | CodeforcesTeamSchema | None = None
    programmingLanguage: str | None = None
    verdict: str | None = None
    testset: str | None = None
    passedTestCount: int | None = None
    timeConsumedMillis: int | None = None
    memoryConsumedBytes: int | None = None
    points: int | None = None
    type_of_member: str | None = None
