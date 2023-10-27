"""API problem"""
from flask import Blueprint

from etr.models.problem import Problem
from etr.services.problem import get_problems_with_contest_id


bp = Blueprint("api_problem", __name__)


@bp.get("/problem/<contest_id>")
def get_problem_with_contest(contest_id: int):
    """Get problem with contest"""

    try:
        problems_schema = get_problems_with_contest_id(contest_id)
    except Exception as exp:
        resp = {
            "status": "error",
            "message": str(exp)
        }
        return resp, 400

    problems = [
        problem_schema.model_dump()
        for problem_schema in problems_schema
    ]

    resp = {
        "status": "ok",
        "problems": problems
    }
    return resp