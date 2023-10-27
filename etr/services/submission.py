from etr.db import get_db
from etr.models.submission import Submission
from etr.models.user import User
from etr.models.problem import Problem
from etr.schemas.submission import SubmissionSchema
from etr.schemas.user import UserSchema
from etr.services.user import get_user
from etr.services.problem import get_problems_with_contest_id
from etr.utils.codeforces.convert import convert_codeforces_submissions_schema
from etr.utils.factory import create_submission_model
from etr.library.codeforces.codeforces_utils import get_submission


def _add_submission_with_schema(submission_schema: SubmissionSchema) -> SubmissionSchema | None:
    try:
        with get_db() as session:
            submission = create_submission_model(**submission_schema.model_dump())
            session.add(submission)
            session.commit()
    except:
        return None
    return submission_schema


def get_submissions(
        handle: str | None = None,
        contest_id: int | None = None,
        problem_index: str | None = None) -> list[dict]:

    print(f"{handle=} {contest_id=} {problem_index=}")

    with get_db() as session:
        user = session.query(User).filter(User.handle == handle).one_or_none()
        if contest_id and problem_index:
            problem = session.query(Problem).filter_by(
                index=problem_index,
                contest_id=contest_id
            ).one_or_none()
        else:
            problem = None

        submissions = session.query(Submission).filter_by(
            author_id=user.id,
            contest_id=contest_id,
            problem_id=problem.id
        ).all()
        # TODO: horror code (refactor)
        for submission in submissions:
            submission.problem
            submission.problem.tags
            submission.author
            submission.team

    submissions = [
        SubmissionSchema.model_validate(submission).model_dump()
        for submission in submissions
    ]

    return submissions


def __get_submission_with_kwargs(**kwargs) -> Submission | None:
    with get_db() as session:
        submissions_db = session.query(Submission).filter_by(
            **kwargs
        ).one_or_none()

    return submissions_db


def _get_submission_with_schema(submission_schema: SubmissionSchema) -> Submission | None:
    filter_params = {
        "id": submission_schema.id,
        "contest_id": submission_schema.contest_id,
        "problem_id": submission_schema.problem.id,
        "team_id": submission_schema.author.id,
        "programming_language": submission_schema.programming_language,
        "verdict": submission_schema.verdict,
        "testset": submission_schema.testset,
        "points": submission_schema.points,
    }

    if "team_name" in submission_schema.author.model_dump():
        filter_params["team_id"] = submission_schema.author.id
    else:
        filter_params["author_id"] = submission_schema.author.id

    submission_db = __get_submission_with_kwargs(**filter_params)

    return submission_db


def update_submission(
    contest_id: int,
    index: str | None,
    handle: str | None,
) -> list[SubmissionSchema] | None:
    user = get_user(handle) if handle else None
    problems = get_problems_with_contest_id(contest_id)

    submissions_schema = convert_codeforces_submissions_schema(
        get_submission(contest_id, handle=handle)
    )

    added_submissions_schemas = []
    for submission_schema in submissions_schema:
        sub = _get_submission_with_schema(submission_schema)
        if sub is None:
            _add_submission_with_schema(submission_schema)
            added_submissions_schemas.append(submission_schema)

    return added_submissions_schemas
