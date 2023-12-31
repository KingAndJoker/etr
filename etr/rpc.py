"""Remote Procedure Call module"""
from threading import Thread

from fastapi import APIRouter

from etr.services.problem import add_missing_problem_with_contest
from etr.services.problem import add_tag_for_problem
from etr.services.contest import update_contest_with_codeforces
from etr.services.contest import get_contests
from etr.services.submission import update_submissions_with_codeforces
from etr.services.user import sync_user_with_dl
from etr.library.codeforces.codeforces_utils import (
    get_contest as get_codeforces_contest,
)
from etr.utils.codeforces.convert import convert_codeforces_problems_schema


# TODO: https://safjan.com/guide-building-python-rpc-server-using-flask/
router = APIRouter()
# bp = Blueprint("rpc", __name__)


@router.get("/contest/{contest_id}")
def update_contest_info(contest_id: int):
    contest_schema = update_contest_with_codeforces(contest_id)

    return contest_schema


@router.get("/submission/{contest_id}")
def update_submission_info(contest_id: int):
    """update submissions with codeforces in db"""

    # TODO: write update submissions for specific user
    Thread(target=update_submissions_with_codeforces, args=(contest_id,)).start()

    return {"status": "ok"}


@router.get("/problem/update_tag")
def update_tag_codeforces():
    contests = get_contests()
    for contest in contests:
        if not contest.type_of_source.startswith("codeforces"):
            continue
        codeforces_contest = get_codeforces_contest(contest.id)
        cf_problems = convert_codeforces_problems_schema(codeforces_contest.problems)
        for problem in contest.problems:
            [cf_problem] = [
                cf_problem
                for cf_problem in cf_problems
                if cf_problem.index == problem.index
            ]
            cf_tags = cf_problem.tags
            for cf_tag in cf_tags:
                add_tag_for_problem(problem_id=problem.id, tag=cf_tag)
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
