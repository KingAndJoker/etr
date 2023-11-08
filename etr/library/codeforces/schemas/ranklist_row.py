from pydantic import BaseModel

from etr.library.codeforces.schemas.user import CodeforcesUserSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.library.codeforces.schemas.problem_result import CodeforcesProblemResult


class CodeforcesRanklistRowSchema(BaseModel):
    party: CodeforcesUserSchema | CodeforcesTeamSchema
    rank: int
    points: float
    penalty: int
    successfulHackCount: int
    unsuccessfulHackCount: int
    problemResults: list[CodeforcesProblemResult]
