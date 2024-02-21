from typing import Any

from fastapi import APIRouter
from fastapi import HTTPException

from etr.services.contest import get_contests
from etr.services.contest import get_contest_table_rows
from etr.services.contest import update_contest
from etr.services.contest import delete_contest_and_deps
from etr.schemas.contest import ContestSchema


router = APIRouter(prefix="/contest", tags=["contests"])


@router.get("/")
def api_get_contests(index: int | None = None, count: int | None = None):
    """get contests"""
    params = {
        key: value
        for key, value in dict(
            contest_index=index,
            contest_count=count,
        ).items()
        if value is not None
    }
    contests_schema = get_contests(**params)

    contests = [contest for contest in contests_schema]
    if index is not None:
        contests = contests[index:]
    if count is not None:
        contests = contests[:count]
    return {"status": "ok", "contests": contests}


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


@router.delete("/contest/{contest_id}")
def api_delete_contest(contest_id: int) -> ContestSchema:
    """удаляет контест с заданным contest_id

    Args:

        contest_id (int): id контеста

    Raises:

        HTTPException: вызывается с статус кодом 404 если контест не найден.

    Returns:
        ContestSchema: схема контеста
    """
    contest = delete_contest_and_deps(contest_id)
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found")
    return contest
