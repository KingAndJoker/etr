from flask import Blueprint, request

from etr.services.submission import get_submissions
from etr.services.submission import delete_submissions
from etr.services.user import get_users
from etr.services.problem import get_problems_with_contest_id
from etr.utils.api.generate import generate_kwargs


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


@bp.delete("/submissions")
def api_delete_submissions():
    id_ = request.args.get("id", None)
    contest_id = request.args.get("contest_id", None)
    author_id = request.args.get("author_id", None)
    team_id = request.args.get("team_id", None)
    problem_id = request.args.get("problem_id", None)
    programming_language = request.args.get("programming_language", None)
    type_of_member = request.args.get("type_of_member", None)

    kwargs = generate_kwargs(
        id=id_,
        contest_id=contest_id,
        author_id=author_id,
        team_id=team_id,
        problem_id=problem_id,
        programming_language=programming_language,
        type_of_member=type_of_member,
    )

    deleted_count = delete_submissions(**kwargs)

    return {
        "status": "ok",
        "count_submissions": deleted_count
    }
