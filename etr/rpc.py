"""Remote Procedure Call module"""
from flask import (
    Blueprint,
    request
)
from sqlalchemy import inspect

from etr.db import get_db
from etr.utils.codeforces_utils import get_contest, get_submission
from etr.models.contest import Contest
from etr.models.submission import Submission
from etr.models.user import User


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__)


@bp.get("/contest/<contest_id>")
def update_contest_info(contest_id: int):
    contest = get_contest(contest_id)
    if contest is None:
        return {"status": "failed"}

    inst = inspect(Contest)
    attr_contest: set[str] = {
        c_attr.key for c_attr in inst.mapper.column_attrs}

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


@bp.get("/submission/<contest_id>")
def update_submission_info(contest_id):
    with get_db() as session:
        users = session.query(User).filter(User.watch).all()

    submissions = list()
    for user in users:
        submissions = get_submission(contest_id, handle=user.handle)

    if submissions is None:
        return {"status": "failed"}

    with get_db() as session:
        for i, submission in enumerate(submissions):
            sub = session.query(Submission).filter(
                Submission.id == submission.id and Submission.contest_id == submission.contest_id
            ).one_or_none()

            if sub is None:
                sub = Submission(**submission.model_dump())
            
            session.add(sub)
        session.commit()

    return {"status": "ok"}
