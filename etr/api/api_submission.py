from flask import Blueprint, request

from etr.services.submission import get_submissions
from etr.services.user import get_users
from etr.services.problem import get_problems_with_contest_id


bp = Blueprint("api_submission", __name__)


@bp.get("/submission")
def api_get_submissions():
    handle = request.args.get("handle", None)
    contest_id = int(request.args.get("contest_id", None))
    problem_index = request.args.get("problem_index", None)

    kwargs = dict()
    # TODO: DRY
    if handle:
        kwargs["author_id"] = get_users(handle=handle)[0].id
    if contest_id:
        kwargs["contest_id"] = contest_id
        if problem_index:
            problems = get_problems_with_contest_id(contest_id)
            problem = [problem for problem in problems if problem.index==problem_index][0]
            kwargs["problem_id"] = problem.id

    submissions = get_submissions(**kwargs)

    return {
        "status": "ok",
        "submissions": [
            submission.model_dump()
            for submission in submissions
        ]
    }
