from flask import Blueprint

from etr.services.contest import get_contests


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
