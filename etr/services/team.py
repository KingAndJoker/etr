""" Team service """
from sqlalchemy.orm.session import Session

from etr.db import get_db
from etr.models.team import Team
from etr.schemas.team import TeamSchema


def __get_teams_db(session: Session, **kwargs) -> list[Team] | None:
    """ get teams from db """
    teams_db = session.query(
        Team
    ).filter_by(
        **kwargs
    ).all()

    return teams_db


def _get_teams_with_kwargs(**kwargs) -> list[TeamSchema]:
    """ get teams from db """
    with get_db() as session:
        teams_db = __get_teams_db(session, **kwargs)

        teams_schema = [
            TeamSchema.model_validate(team)
            for team in teams_db
        ]

    return teams_schema


def get_teams(**kwargs) -> list[TeamSchema]:
    """
    etr.services.team.get_teams
    =====
    Get teams from db

    :param kwargs: filter params
    :return: list of teams
    :rtype: list[TeamSchema]
    :raises: None

    Example::
    =====
    >>> get_teams(team_name="team_name")
    """

    teams_schema = _get_teams_with_kwargs(**kwargs)

    return teams_schema
