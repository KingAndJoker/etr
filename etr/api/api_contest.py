from typing import Any

from fastapi import APIRouter

from etr.services.contest import get_contests, get_contest_table_rows
from etr.services.contest import update_contest


router = APIRouter(prefix="/contests", tags=["contests"])


@router.get("/")
def api_get_contests():
    """get contests"""
    contests_schema = get_contests()

    return {"status": "ok", "contests": [contest for contest in contests_schema]}


@router.get("/{contest_id}/table")
def api_get_table_contest(contest_id: int):
    contest = get_contests(id=contest_id)[0]
    rows = get_contest_table_rows(contest_id)

    response = {"status": "ok", "contest": contest, "rows": []}

    for row in rows:
        if "user" in row:
            response["rows"].append(
                {"user": row["user"], "submissions": row["submissions"]}
            )
        else:
            response["rows"].append(
                {"team": row["team"], "submissions": row["submissions"]}
            )

    return response


@router.patch("/contest/{contest_id}")
def api_update_contest(contest_id: int, contest_update_fields: dict[str, Any]):
    contest = update_contest(contest_id, **contest_update_fields)
    if contest is None:
        return {"status": "error"}

    return {"status": "ok", "contest": contest}
