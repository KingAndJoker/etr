from fastapi import APIRouter

from etr.services.submission import get_submissions
from etr.services.submission import delete_submissions
from etr.schemas.user import ContestantType
from etr.utils.api.generate import generate_kwargs


router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get("/")
def api_get_submissions(
    handle: str | None = None,
    contest_id: int | None = None,
    problem_index: str | None = None,
):
    kwargs = generate_kwargs(
        handle=handle, contest_id=contest_id, problem_index=problem_index
    )
    submissions = get_submissions(**kwargs)

    return {"status": "ok", "submissions": submissions}


@router.delete("/")
def api_delete_submissions(
    id_: int | None = None,
    contest_id: int | None = None,
    author_id: int | None = None,
    team_id: int | None = None,
    problem_id: int | None = None,
    programming_language: str | None = None,
    type_of_member: ContestantType | None = None,
):
    kwargs = generate_kwargs(
        id_=id_,
        contest_id=contest_id,
        author_id=author_id,
        team_id=team_id,
        problem_id=problem_id,
        programming_language=programming_language,
        type_of_member=type_of_member,
    )

    deleted_count = delete_submissions(**kwargs)

    return {"status": "ok", "count_submissions": deleted_count}
