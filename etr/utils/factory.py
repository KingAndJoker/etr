""" factory methods """
from sqlalchemy import inspect

from etr.models.contest import Contest
from etr.models.problem import Problem, Tag
from etr.models.submission import Submission
from etr.schemas.contest import ContestSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.submission import SubmissionSchema
from etr.db import get_db


def create_contest_model(**kwargs) -> Contest | None:
    """ factory method returns Contest model from fields equal to kwargs """

    try:
        check_contest = ContestSchema(**kwargs)
    except:
        return None

    inst = inspect(Contest)
    attr_contest: set[str] = {
        c_attr.key for c_attr in inst.mapper.column_attrs
    }

    try:
        contest = Contest()
        for field, value in kwargs.items():
            if field in attr_contest:
                setattr(contest, field, value)
    except:
        return None

    return contest


def create_problem_model(**kwargs) -> Problem | None:
    """ factory method returns Problem model from fields equal to kwargs """

    try:
        check_problem = ProblemSchema(**kwargs)
    except:
        return None

    # TODO: add Tags

    inst = inspect(Problem)
    attr_problem: set[str] = {
        p_attr.key for p_attr in inst.mapper.column_attrs
    }

    try:
        problem = Problem()
        for field, value in kwargs.items():
            if field in attr_problem:
                setattr(problem, field, value)
    except:
        return None

    return problem


def create_submission_model(**kwargs) -> Submission | None:
    """ factory method returns Submission model from fields equal to kwargs """

    try:
        check_submission = SubmissionSchema(**kwargs)
    except:
        return None

    inst = inspect(Submission)
    attr_submission: set[str] = {
        s_attr.key for s_attr in inst.mapper.column_attrs
    }

    try:
        submission = Submission()
        for field, value in kwargs.items():
            if field in attr_submission:
                setattr(submission, field, value)
        
        if submission.problem_id is None:
            submission.problem_id = kwargs["problem"].id
    except:
        return None

    return submission
