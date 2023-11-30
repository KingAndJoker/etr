"""Remote Procedure Call module"""
from threading import Thread

# from flask import (
#     Blueprint,
#     request
# )
from fastapi import APIRouter

from etr.services.problem import add_missing_problem_with_contest
from etr.services.contest import update_contest_with_codeforces
from etr.services.submission import update_submissions_with_codeforces
from etr.services.user import sync_user_with_dl


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
router = APIRouter()
# bp = Blueprint("rpc", __name__)


@router.get("/contest/{contest_id}")
def update_contest_info(contest_id: int):
    contest_schema = update_contest_with_codeforces(contest_id)

    return contest_schema


@router.get("/submission/{contest_id}")
def update_submission_info(contest_id: int):
    """ update submissions with codeforces in db """

    # TODO: write update submissions for specific user
    Thread(target = update_submissions_with_codeforces, args=(contest_id,)).start()
    
    return {"status": "ok"}


@router.get("/problem/{contest_id}")
def update_missing_problems(contest_id: int):
    added_problems = add_missing_problem_with_contest(contest_id)
    return added_problems


@router.get("/user/swdl")
def sync_with_dl():
    try:
        sync_user_with_dl()
    except Exception as exp:
        raise

    return {"status": "ok"}
