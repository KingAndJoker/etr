from flask import Blueprint, request

from etr.services.submission import get_submissions


bp = Blueprint("api_submission", __name__)


@bp.get("/submission")
def api_get_submissions():
    handle = request.args.get("handle", None)
    contest_id = int(request.args.get("contest_id", None))
    problem_index = request.args.get("problem_index", None)

    submissions = get_submissions(handle, contest_id, problem_index)

    return submissions
