import copy

from sqlalchemy.orm import Session

from etr.db import get_db
from etr.models.submission import Submission
from etr.schemas.submission import SubmissionSchema
from etr.utils.factory import create_submission_model
from etr.services.user import get_users
from etr.services.problem import get_problems_with_contest_id
from etr.library.codeforces.codeforces_utils import get_submission as cf_get_submission
from etr.utils.codeforces.convert import convert_codeforces_submission_schema


def __get_submissions_db(session: Session, **kwargs) -> list[Submission] | None:
    """ get submissions from db """
    submissions_db = session.query(
        Submission
    ).filter_by(
        **kwargs
    ).all()

    return submissions_db


def __get_submission_db(session: Session, **kwargs) -> Submission | None:
    """ get submissions from db """
    submissions_db = session.query(
        Submission
    ).filter_by(
        **kwargs
    ).one_or_none()

    return submissions_db


def __add_submission_db(session: Session, **kwargs) -> Submission:
    """ add submission to db """
    try:
        submission_db = create_submission_model(**kwargs)
        session.add(submission_db)
        session.commit()
    except:
        session.rollback()
        return None

    return submission_db


def __update_submission_db(session: Session, submission: Submission, **kwargs) -> Submission | None:
    """ update submission in db """
    for field, value in kwargs.items():
        setattr(submission, field, value)
    session.add(submission)
    session.commit()

    submission = session.query(Submission).filter_by(id=submission.id, **kwargs).one_or_none()

    return submission


def _check_submission_update(submission_schema: SubmissionSchema, **kwargs) -> bool:
    """ check if submission can be updated """
    try:
        copy_submission_schema = copy.deepcopy(submission_schema)
        for key, value in kwargs.items():
            setattr(copy_submission_schema, key, value)
        
        check_submission_schema = SubmissionSchema(**copy_submission_schema.model_dump())
    except:
        return False

    return True


def _update_submission_db(submission_schema: SubmissionSchema, **kwargs) -> SubmissionSchema | None:
    """ update submission in db """

    if not _check_submission_update(submission_schema, **kwargs):
        return None
    
    with get_db() as session:
        submission_db = __get_submission_db(session, id=submission_schema.id)

        if submission_db is None:
            return None

        submission_db = __update_submission_db(session, submission_db, **kwargs)

        submission_db = __get_submission_db(session, id=submission_schema.id)
        submission_return_schema = SubmissionSchema.model_validate(submission_db)

    return submission_return_schema


def _add_submission_with_schema(submission_schema: SubmissionSchema) -> SubmissionSchema | None:
    # TODO: DRY params
    params = submission_schema.model_dump()
    if "problem" in params:
        problems = get_problems_with_contest_id(params["contest_id"])
        problem = [problem for problem in problems if problem.index==submission_schema.problem.index][0]
        params["problem_id"] = problem.id
        params.pop("problem")

    with get_db() as session:
        __add_submission_db(session, **params)
        submission_db = __get_submission_db(session, id=params["id"])
        if submission_db is None:
            return None
        submission_return_schema = SubmissionSchema.model_validate(submission_db)
    return submission_return_schema


def _get_submissions_with_kwargs(**kwargs) -> list[SubmissionSchema] | None:
    with get_db() as session:
        submissions_db = __get_submissions_db(session, **kwargs)

        submissions_schema = [
            SubmissionSchema.model_validate(submission)
            for submission in submissions_db
        ]

    return submissions_schema


def _get_submission_with_kwargs(**kwargs) -> SubmissionSchema | None:
    with get_db() as session:
        submission_db = __get_submission_db(session, **kwargs)

        if submission_db is None:
            return None
        
        submission_schema = SubmissionSchema.model_validate(submission_db)

    return submission_schema


def get_submissions(
        **kwargs
    ) -> list[SubmissionSchema]:
    """ get submissions from db """
    submissions_schema = _get_submissions_with_kwargs(**kwargs)

    return submissions_schema


def get_submission(**kwargs) -> SubmissionSchema | None:
    """ get submission from db """
    submission_schema = _get_submission_with_kwargs(**kwargs)

    return submission_schema


def update_submission(
    submission_id: int,
    **kwargs
) -> SubmissionSchema | None:
    """ update submission in db """

    submission_schema = get_submission(id=submission_id)

    if submission_schema is None:
        return None
    
    submission_schema = _update_submission_db(submission_schema, **kwargs)

    return submission_schema


def update_submissions_with_codeforces(contest_id: int) -> list[SubmissionSchema]:
    users = get_users()

    submissions = list()

    for user in users:
        cf_subs = cf_get_submission(contest_id, handle=user.handle)
        submissions = []
        if cf_subs:
            submissions = [
                convert_codeforces_submission_schema(cf_sub)
                for cf_sub in cf_subs
            ]

        for submission in submissions:
            params = make_params_for_submission(submission)
            sub_is_exist = get_submission(**params)
            if sub_is_exist is not None:
                continue
            sub_add = _add_submission_with_schema(submission)
            if sub_add is None:
                continue
            submissions.append(sub_add)

    return submissions


def make_params_for_submission(submission: SubmissionSchema) -> dict:
    params = submission.model_dump()

    if "problem" in params: params.pop("problem")
    if "author" in params: params.pop("author")

    return params
