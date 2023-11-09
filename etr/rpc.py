"""Remote Procedure Call module"""
from flask import (
    Blueprint,
    request
)

from etr.services.problem import add_missing_problem_with_contest
from etr.services.contest import update_contest_with_codeforces
from etr.services.submission import update_submissions_with_codeforces
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
    """ update submissions with codeforces in db """

    response = dict()
    status = "ok"
    submissions_schema = update_submissions_with_codeforces(
        contest_id
    )
    
    response["status"] = status
    response["result"] = [
        submission.model_dump()
        for submission in submissions_schema
    ]

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
    except Exception as exp:
        raise

    return {"status": "ok"}
