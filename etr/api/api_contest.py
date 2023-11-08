from flask import Blueprint

from etr.services.contest import get_contests, get_contest_table_rows
from etr.utils.contest import get_count_success_tasks


bp = Blueprint("api_contest", __name__)


@bp.get("/contest")
def api_get_contests():
    """get contests"""
    contests_schema = get_contests()

    return {
        "status": "ok",
        "contests": [
            contest_schema.model_dump()
            for contest_schema in contests_schema
        ]
    }


@bp.get("/contest/<int:contest_id>/table")
def api_get_table_contest(contest_id: int):
    contest = get_contests(id=contest_id)[0]
    rows = get_contest_table_rows(contest_id)

    decorated = [
        (get_count_success_tasks(row["submissions"]),
         i,
         row)
        for i, row in enumerate(rows)
    ]
    decorated.sort()
    decorated.reverse()
    rows = [
        row
        for _, _, row in decorated
    ]

    return {
        "status": "ok",
        "contest": contest.model_dump(),
        "rows": [
            {
                "user": row["user"].model_dump(),
                "submissions": [
                    submission.model_dump()
                    for submission in row["submissions"]
                ]
            }
            for row in rows
        ]
    }
