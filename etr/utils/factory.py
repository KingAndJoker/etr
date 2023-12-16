""" factory methods """
from sqlalchemy import inspect

from etr.models.contest import ContestOrm
from etr.models.problem import ProblemOrm, TagOrm
from etr.models.submission import SubmissionOrm
from etr.models.user import UserOrm
from etr.schemas.contest import ContestSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.submission import SubmissionSchema
from etr.schemas.user import UserSchema
from etr import db


def create_contest_model(**kwargs) -> ContestOrm | None:
    """ factory method returns Contest model from fields equal to kwargs """

    try:
        check_contest = ContestSchema(**kwargs)
    except:
        return None

    inst = inspect(ContestOrm)
    attr_contest: set[str] = {
        c_attr.key for c_attr in inst.mapper.column_attrs
    }

    try:
        contest = ContestOrm()
        for field, value in kwargs.items():
            if field in attr_contest:
                setattr(contest, field, value)
    except:
        return None

    return contest


def create_problem_model(**kwargs) -> ProblemOrm | None:
    """ factory method returns Problem model from fields equal to kwargs """

    try:
        check_problem = ProblemSchema(**kwargs)
    except:
        return None

    # TODO: add Tags

    inst = inspect(ProblemOrm)
    attr_problem: set[str] = {
        p_attr.key for p_attr in inst.mapper.column_attrs
    }

    try:
        problem = ProblemOrm()
        for field, value in kwargs.items():
            if field in attr_problem:
                setattr(problem, field, value)
    except:
        return None

    return problem


def create_submission_model(**kwargs) -> SubmissionOrm | None:
    """ factory method returns Submission model from fields equal to kwargs """

    try:
        check_submission = SubmissionSchema(**kwargs)
    except:
        return None

    inst = inspect(SubmissionOrm)
    attr_submission: set[str] = {
        s_attr.key for s_attr in inst.mapper.column_attrs
    }

    try:
        submission = SubmissionOrm()
        for field, value in kwargs.items():
            if field in attr_submission:
                setattr(submission, field, value)
        
        if submission.problem_id is None:
            if "problem" in kwargs:
                submission.problem_id = kwargs["problem"].id # get_problem(...)
            else:
                with db.SessionLocal() as session:
                    problem = session.query(ProblemOrm).filter_by(
                        contest_id = submission.contest_id,
                        index = kwargs["problem"]["index"]
                    ).one_or_none()
                submission.problem_id = problem.id

        if "author" in kwargs:
            if "teamId" in kwargs["author"]:
                submission.team_id = kwargs["author"]["teamId"]
            else:
                with db.SessionLocal() as session:
                    user = session.query(UserOrm).filter(UserOrm.handle == kwargs["author"]["handle"]).first()
                    submission.author_id = user.id
    except:
        return None

    return submission


def create_user_model(**kwargs) -> UserOrm | None:
    """ factory method returns User model from fields equal to kwargs """

    try:
        check_user = UserSchema(**kwargs)
    except:
        return None

    inst = inspect(UserOrm)
    attr_user: set[str] = {
        u_attr.key for u_attr in inst.mapper.column_attrs
    }

    try:
        user = UserOrm()
        for field, value in kwargs.items():
            if field in attr_user:
                setattr(user, field, value)
    except:
        return None

    return user
