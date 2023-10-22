from etr.db import get_db
from etr.models.submission import Submission
from etr.models.user import User
from etr.models.problem import Problem
from etr.schemas.submission import SubmissionSchema


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
