from pydantic import BaseModel


class CodeforcesProblemResult(BaseModel):
    points: float
    penalty: int | None = None
    rejectedAttemptCount: int
    type: str
    bestSubmissionTimeSeconds: int
