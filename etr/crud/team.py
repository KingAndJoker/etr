""" Team crud """
from sqlalchemy.orm.session import Session

from etr import db
from etr.models.team import TeamOrm
from etr.models.user import UserOrm
from etr.schemas.team import TeamSchema
from etr.crud.user import get_user
from etr.crud.user import get_users
from etr.crud.user import add_user


def __get_teams_db(session: Session, **kwargs) -> list[TeamOrm] | None:
    """ get teams from db """
    teams_db = session.query(
        TeamOrm
    ).filter_by(
        **kwargs
    ).all()

    return teams_db


def _get_teams_with_kwargs(**kwargs) -> list[TeamSchema]:
    """ get teams from db """
    with db.SessionLocal() as session:
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


def get_teams_with_handle_member(handle: str) -> list[TeamSchema]:
    """
    get_teams_with_handle_member
    =====
    return all teams for user with handle.
    :param handle: str, handle of user
    :return: list of TeamSchema
    :rtype: list[TeamSchema]
    :raises: None

    Example::
    =====
    >>> get_teams_with_handle_member("tourist")
    """
    teams = []
    for team in get_teams():
        if handle in (user.handle for user in team.users):
            teams.append(team)

    return teams


def __add_team(session: Session, **kwargs) -> TeamOrm | None:
    """ add team to db """
    team = TeamOrm(**kwargs)

    session.add(team)
    session.commit()

    return team


def _check_members(team_schema: TeamSchema) -> None:
    """
    check members in team
    if user not in db, add him
    """
    missing_users = []
    members = team_schema.users
    for member in members:
        user_schema = get_user(
            handle=member.handle
        )
        if user_schema is None:
            missing_users.append(member.handle)
        user_schema = add_user(
            handle=member.handle, lang="ru", watch=False
        )


def _add_team_db(team_schema: TeamSchema) -> TeamSchema | None:
    """ add team to db """
    with db.SessionLocal() as session:
        team_dump = team_schema.model_dump()
        for i, member in enumerate(team_dump["users"]):
            # TODO: rewrite without session.query ...
            team_dump["users"][i] = session.query(UserOrm).filter_by(handle=member["handle"]).one()
        team_db = __add_team(session, **team_dump)
        team_schema = TeamSchema.model_validate(team_db)

        return team_schema


def add_team_with_schema(team: TeamSchema) -> TeamSchema:
    """
    etr.services.team.add_team_with_schema
    =====
    Add team to db

    :param team: team schema
    :type team: TeamSchema
    :return: added team
    :rtype: TeamSchema
    :raises: None

    Example::
    =====
    >>> add_team_with_schema(team_schema)
    """

    _check_members(team)
    team_schema = _add_team_db(team)

    return team_schema


def is_our_team_json(author: dict) -> bool:
    """check team is our

    Args:
        author (dict): https://codeforces.com/apiHelp/objects#Party

    Returns:
        bool: if user (one or more) is ours then returns True
    """
    users = get_users()
    handles = [user.handle.lower() for user in users]
    for member in author["members"]:
        if member["handle"].lower() in handles:
            return True
    return False
