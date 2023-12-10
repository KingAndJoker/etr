"""API problem"""
from fastapi import APIRouter

from etr.services.problem import get_problems_with_contest_id, get_problems


router = APIRouter(prefix="/problem", tags=["problems"])


@router.get("/")
def api_get_problems(
    id_: int | None = None,
    contest_id: int | None = None,
    problemset_name: str | None = None,
    index: str | None = None,
):
    params = {
        "id": id_,
        "contest_id": contest_id,
        "problemset_name": problemset_name,
        "index": index,
    }
    params = {key: value for key, value in params.items() if value is not None}
    problems = get_problems(**params)
    return {
        "status": "ok",
        "problems": [problem.model_dump() for problem in problems]
    }


@router.get("/{contest_id}")
def get_problem_with_contest(contest_id: int):
    """Get problem with contest"""

    problems_schema = get_problems_with_contest_id(contest_id)
    return {"status": "ok", "problems": problems_schema}
