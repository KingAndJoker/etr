"""Submission schema file"""
from pydantic import BaseModel, ConfigDict


class SubmissionSchema(BaseModel):
    """
    Submission pydantic schema
    without field:
      author
      testset
      partial problem

    https://codeforces.com/apiHelp/objects#Submission
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    contestId: int | None = None
    creationTimeSeconds: int | None = None
    relativeTimeSeconds: int | None = None
    problemName: str | None = None
    problemIndex: str | None = None
    programmingLanguage: str | None = None
    verdict: str | None = None
    passedTestCount: int | None = None
    timeConsumedMillis: int | None = None
    memoryConsumedBytes: int | None = None
    points: int | None = None
