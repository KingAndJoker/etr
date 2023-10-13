"""Remote Procedure Call module"""
from flask import (
    Blueprint,
    request
)
from sqlalchemy import inspect

from etr.db import get_db
from etr.utils.codeforces_utils import get_contest
from etr.models.contest import Contest


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__)


@bp.get("/contest/<contest_id>")
def update_contest_info(contest_id: int):
    contest = get_contest(contest_id)
    if contest is None:
        return {"status": "failed"}

    inst = inspect(Contest)
    attr_contest: set[str] = {c_attr.key for c_attr in inst.mapper.column_attrs}

    with get_db() as session:
        contest_dict = contest.model_dump(include=attr_contest)
        contest_db = session.query(Contest).filter(
            Contest.id == contest_id
        ).one_or_none()

        if contest_db is None:
            contest_db = Contest(**contest_dict)
        else:
            for field, value in contest_dict.items():
                setattr(contest_db, field, value)

        session.add(contest_db)
        session.commit()

    return {"status": "ok"}
