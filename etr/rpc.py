"""Remote Procedure Call module"""
import copy
from flask import (
    Blueprint,
    request
)
from sqlalchemy import inspect

from etr.db import get_db
from etr.library.codeforces.codeforces_utils import get_contest, get_submission
from etr.models.contest import Contest
from etr.models.submission import Submission
from etr.models.user import User
from etr.schemas.submission import SubmissionSchema
from etr.utils.codeforces.convert import (
    convert_codeforces_contest_schema,
    convert_codeforces_submissions_schema
)
from etr.utils.factory import (
    create_contest_model,
    create_submission_model
)
from etr.services.problem import add_missing_problem_with_contest


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__)


@bp.get("/contest/<contest_id>")
def update_contest_info(contest_id: int):
    contest = convert_codeforces_contest_schema(
        get_contest(contest_id)
    )
    if contest is None:
        return {"status": "failed"}

    with get_db() as session:
        contest_db = session.query(Contest).filter(
            Contest.id == contest_id
        ).one_or_none()

        if contest_db is None:
            contest_db = create_contest_model(**contest.model_dump())
        else:
            for field, value in contest.model_dump().items():
                setattr(contest_db, field, value)

        session.add(contest_db)
        session.commit()

    return {"status": "ok"}


@bp.get("/submission/<contest_id>")
def update_submission_info(contest_id):
    with get_db() as session:
        users = session.query(User).filter(User.watch).all()

    submissions_schema: list[SubmissionSchema] = list()
    for user in users:
        submissions_schema += convert_codeforces_submissions_schema(
            get_submission(contest_id, handle=user.handle)
        )

    with get_db() as session:
        for submission_schema in submissions_schema:
            sub = session.query(Submission).filter(
                Submission.id == submission_schema.id and Submission.contest_id == contest_id
            ).one_or_none()

            if sub is None:
                sub = create_submission_model(**submission_schema.model_dump())

                if sub is not None:
                    session.add(sub)
                    session.commit()

    return {
        "status": "ok",
        "result": [
            submission_schema.model_dump()
            for submission_schema in submissions_schema
        ]
    }


@bp.get("/problem/<contest_id>")
def update_missing_problems(contest_id: int):
    added_problems = add_missing_problem_with_contest(contest_id)
    problems = [
        added_problem.model_dump()
        for added_problem in added_problems
    ]

    return {
        "status": "ok",
        "result": added_problems
    }
