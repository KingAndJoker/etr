import time
import copy

from sqlalchemy.orm import Session

from etr import db
from etr.models.submission import SubmissionOrm
from etr.schemas.submission import SubmissionSchema
from etr.schemas.team import TeamSchema
from etr.schemas.user import UserSchema
from etr.utils.factory import create_submission_model
from etr.services.problem import get_problems_with_contest_id
from etr.crud.team import get_teams
from etr.crud.team import add_team_with_schema
from etr.crud.team import update_team
from etr.crud.user import get_user


def __get_submissions_db(session: Session,
                         min_creation_time_seconds: int | None = None,
                         max_creation_time_seconds: int | None = None,
                         **kwargs) -> list[SubmissionOrm] | None:
    """get submissions from db"""
    result = session.query(SubmissionOrm).filter_by(**kwargs)
    if min_creation_time_seconds:
        result = result.filter(SubmissionOrm.creation_time_seconds >= min_creation_time_seconds)
    if max_creation_time_seconds:
        result = result.filter(SubmissionOrm.creation_time_seconds <= max_creation_time_seconds)

    return result.all()


def __get_submission_db(session: Session, **kwargs) -> SubmissionOrm | None:
    """get submissions from db"""
    return session.query(SubmissionOrm).filter_by(**kwargs).one_or_none()


def __add_submission_db(session: Session, **kwargs) -> SubmissionOrm:
    """add submission to db"""
    try:
        submission_db = create_submission_model(**kwargs)
        session.add(submission_db)
        session.commit()
    except:
        session.rollback()
        return None
    return submission_db


def __update_submission_db(
    session: Session, submission: SubmissionOrm, **kwargs
) -> SubmissionOrm | None:
    """update submission in db"""
    for field, value in kwargs.items():
        if field != "problem" and field != "author" and field != "team":
            setattr(submission, field, value)
    session.add(submission)
    session.commit()

    submission = (
        session.query(SubmissionOrm).filter_by(id=submission.id).one_or_none()
    )

    return submission


def _check_submission_update(submission_schema: SubmissionSchema, **kwargs) -> bool:
    """check if submission can be updated"""
    try:
        copy_submission_schema = copy.deepcopy(submission_schema)
        for key, value in kwargs.items():
            setattr(copy_submission_schema, key, value)

        check_submission_schema = SubmissionSchema(
            **copy_submission_schema.model_dump()
        )
    except:
        return False

    return True


def _update_submission_db(
    submission_schema: SubmissionSchema, **kwargs
) -> SubmissionSchema | None:
    """update submission in db"""

    if not _check_submission_update(submission_schema, **kwargs):
        return None

    with db.SessionLocal() as session:
        submission_db = __get_submission_db(session, id=submission_schema.id)

        if submission_db is None:
            return None

        submission_db = __update_submission_db(
            session, submission_db, **kwargs)

        submission_db = __get_submission_db(session, id=submission_schema.id)
        submission_return_schema = SubmissionSchema.model_validate(
            submission_db)

    return submission_return_schema


def _add_submission_with_schema(
    submission_schema: SubmissionSchema,
) -> SubmissionSchema | None:
    # TODO: DRY params
    params = submission_schema.model_dump()
    if "problem" in params:
        problems = get_problems_with_contest_id(params["contest_id"])
        problem = [
            problem
            for problem in problems
            if problem.index == submission_schema.problem.index
        ][0]
        params["problem_id"] = problem.id
        params.pop("problem")

    # TODO: убрать обращения к crud user во избежание циклических импортов
    if isinstance(submission_schema.author, TeamSchema):
        teams = get_teams(id=submission_schema.author.id)
        if teams == []:
            team = add_team_with_schema(submission_schema.author)
        else:
            team = update_team(
                id=submission_schema.author.id,
                team_name=submission_schema.author.team_name
            )
        params["team_id"] = team.id
        params.pop("author")
    elif isinstance(submission_schema.author, UserSchema):
        user = get_user(submission_schema.author.handle)
        params["author_id"] = user.id
        params.pop("author")

    author_id = params.get("author_id", None)
    team_id = params.get("team_id", None)
    if author_id is None and team_id is None:
        # TODO: raise Exception
        return None

    with db.SessionLocal() as session:
        __add_submission_db(session, **params)
        submission_db = __get_submission_db(session, id=params["id"])
        if submission_db is None:
            return None
        submission_return_schema = SubmissionSchema.model_validate(submission_db)
    return submission_return_schema


def _get_submissions_with_kwargs(**kwargs) -> list[SubmissionSchema] | None:
    with db.SessionLocal() as session:
        submissions_db = __get_submissions_db(session, **kwargs)

        submissions_schema = [
            SubmissionSchema.model_validate(submission) for submission in submissions_db
        ]

    return submissions_schema


def _get_submission_with_kwargs(**kwargs) -> SubmissionSchema | None:
    with db.SessionLocal() as session:
        submission_db = __get_submission_db(session, **kwargs)

        if submission_db is None:
            return None

        submission_schema = SubmissionSchema.model_validate(submission_db)

    return submission_schema


def get_submissions(**kwargs) -> list[SubmissionSchema]:
    """get submissions from db"""
    submissions_schema = _get_submissions_with_kwargs(**kwargs)
    if submissions_schema is None:
        return []

    return submissions_schema


def get_submission(**kwargs) -> SubmissionSchema | None:
    """get submission from db"""
    submission_schema = _get_submission_with_kwargs(**kwargs)

    return submission_schema


def update_submission(submission_id: int, **kwargs) -> SubmissionSchema | None:
    """update submission in db"""

    submission_schema = get_submission(id=submission_id)

    if submission_schema is None:
        return None

    submission_schema = _update_submission_db(submission_schema, **kwargs)

    return submission_schema


def is_our_submission(
    submission: dict, handles: list[str], teams_id: list[int]
) -> bool:
    """return True if the submission contains a user or team from the database

    Args:
        submission (SubmissionSchema): checking submission
        handles (list[str]): handles users
        teams_id (list[int]): id of teams

    Returns:
        bool: True if the submission contains user or team from the database
    """
    if "teamId" not in submission["author"]:
        if submission["author"]["members"] != []:
            return submission["author"]["members"][0]["handle"].lower() in handles
        else:
            return False
    else:
        return submission["author"]["teamId"] in teams_id


def __delete_submissions(session: Session, **kwargs) -> list[SubmissionSchema]:
    cnt_deleted = session.query(SubmissionOrm).filter_by(**kwargs).delete()
    return cnt_deleted


def _delete_submissions(**kwargs) -> int:
    with db.SessionLocal() as session:
        cnt = __delete_submissions(session, **kwargs)
        session.commit()
    return cnt


def delete_submissions(**kwargs) -> int:
    """delete submissions from db

    Args:
        id (int): id of submission
        contest_id (int): id of contest
        author_id (int): id of author
        team_id (int): id of team
        problem_id (int): id of problem
        programming_language (str): programming language
        type_of_member (str): type of member

    Returns:
        int: count of deleted submissions
    """
    cnt_deleted_submissions = _delete_submissions(**kwargs)
    return cnt_deleted_submissions


def add_submission_with_schema(submission: SubmissionSchema) -> SubmissionSchema:
    return _add_submission_with_schema(submission)
