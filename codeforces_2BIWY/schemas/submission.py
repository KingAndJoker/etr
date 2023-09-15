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
    contestId: int
    creationTimeSeconds: int
    relativeTimeSeconds: int
    problemName: str
    problemIndex: str
    programmingLanguage: str
    verdict: str
    passedTestCount: int
    timeConsumedMillis: int
    memoryConsumedBytes: int
    points: int
