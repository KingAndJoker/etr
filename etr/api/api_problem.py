"""API problem"""
from fastapi import APIRouter

from etr.services.problem import get_problems_with_contest_id


router = APIRouter(
    prefix="/problem",
    tags=["problems"]
)


@router.get("/{contest_id}")
def get_problem_with_contest(contest_id: int):
    """Get problem with contest"""

    problems_schema = get_problems_with_contest_id(contest_id)
    return problems_schema
