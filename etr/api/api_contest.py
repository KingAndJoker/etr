# from flask import Blueprint
from fastapi import APIRouter

from etr.services.contest import get_contests, get_contest_table_rows
from etr.utils.contest import get_count_success_tasks


# bp = Blueprint("api_contest", __name__)
router = APIRouter(
    prefix="/contests",
    tags=["contests"]
)


@router.get("/")
def api_get_contests():
    """get contests"""
    contests_schema = get_contests()

    return contests_schema


@router.get("/{contest_id}/table")
def api_get_table_contest(contest_id: int):
    contest = get_contests(id=contest_id)[0]
    rows = get_contest_table_rows(contest_id)

    response = {
        "status": "ok",
        "contest": contest.model_dump(),
        "rows": []
    }

    for row in rows:
        if "user" in row:
            response["rows"].append({
                "user": row["user"],
                "submissions": row["submissions"]
            })
        else:
            response["rows"].append({
                "team": row["team"],
                "submissions": row["submissions"]
            })

    return response
