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
from etr.services.contest import update_contest
from etr.services.submission import update_submission


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__)


@bp.get("/contest/<contest_id>")
def update_contest_info(contest_id: int):
    contest_schema = update_contest(contest_id)

    response = dict()
    status = "ok"

    if contest_schema is None:
        status = "error"

    else:
        contest = contest_schema.model_dump()
        response["result"] = contest

    response["status"] = status

    return response


@bp.get("/submission/<contest_id>")
def update_submission_info(contest_id: int):
    handle = request.args.get("handle", None)
    index = request.args.get("index", None)

    response = dict()
    status = "ok"
    submissions_schema = update_submission(
        contest_id,
        handle=handle,
        index=index
    )
    if submissions_schema is None:
        status = "error"
    else:
        submissions = [
            submission_schema.model_dump()
            for submission_schema in submissions_schema if submission_schema is not None
        ]
        response["result"] = submissions

    response["status"] = status

    return response


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
