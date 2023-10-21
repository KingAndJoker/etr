""" factory methods """
from sqlalchemy import inspect

from etr.models.contest import Contest
from etr.schemas.contest import ContestSchema


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
