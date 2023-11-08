from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.ranklist_row import CodeforcesRanklistRowSchema


def standings(contest_id: int,
              as_manager: bool | None = None,
              from_: int | None = None,
              count: int | None = None,
              handles: str | None = None,
              room: int | None = None,
              show_unofficial: bool | None = None,
              lang: str="ru") -> tuple[CodeforcesContestSchema, list[CodeforcesProblemSchema], CodeforcesRanklistRowSchema]:
    pass
