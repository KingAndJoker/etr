"""Remote Procedure Call module"""
from flask import (
    Blueprint,
    request
)

from etr.services.problem import add_missing_problem_with_contest
from etr.services.contest import update_contest_with_codeforces
from etr.services.submission import update_submission
from etr.services.user import sync_user_with_dl


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
bp = Blueprint("rpc", __name__)


@bp.get("/contest/<contest_id>")
def update_contest_info(contest_id: int):
    contest_schema = update_contest_with_codeforces(contest_id)

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


@bp.get("/user/swdl")
def sync_with_dl():
    try:
        sync_user_with_dl()
    except:
        return {"status", "error"}

    return {"status": "ok"}
