""" factory methods """
from sqlalchemy import inspect

from etr.models.contest import Contest
from etr.models.problem import Problem, Tag
from etr.schemas.contest import ContestSchema
from etr.schemas.problem import ProblemSchema
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
