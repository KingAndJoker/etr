"""API problem"""
from flask import Blueprint, request

from etr.services.problem import get_problems_with_contest_id, get_problems


bp = Blueprint("api_problem", __name__)


@bp.get("/problem")
def api_get_problems():
    params = {
        "id": request.args.get("id", None),
        "contest_id": request.args.get("contest_id", None),
        "problemset_name": request.args.get("problemset_name", None),
        "index": request.args.get("index", None),
    }
    if params["id"]:
        params["id"] = int(params["id"])
    if params["contest_id"]:
        params["contest_id"] = int(params["contest_id"])
    print(params)
    params = {
        key: value
        for key, value in params.items()
        if value is not None
    }
    problems = get_problems(**params)
    return {
        "status": "ok",
        "problems": [
            problem.model_dump() for problem in problems
        ]
    }


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
