""" contest services """
import logging

from etr.schemas.contest import ContestSchema
from etr.schemas.submission import SubmissionSchema
from etr.library.codeforces import contest as codeforces_contest
from etr.library.codeforces.codeforces_utils import (
    get_contest as get_contest_with_codeforces,
)
from etr.crud.problem import add_problems_with_cf
from etr.crud.user import get_users
from etr.crud.user import get_user
from etr.crud.team import get_teams_with_handle_member
from etr.crud.submission import get_submissions
from etr.crud.submission import update_submission
from etr.crud.submission import add_submission_with_schema
from etr.crud.contest import get_contests
from etr.crud.contest import add_contest_with_schema
from etr.crud.contest import update_contest
from etr.crud.contest import delete_contest
from etr.crud.submission import delete_submissions
from etr.crud.problem import delete_problems
from etr.crud.problem import get_problems
from etr.utils.codeforces.convert import convert_codeforces_contest_schema
from etr.utils.codeforces.convert import convert_codeforces_submissions_schema


def get_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    """get contest from codeforces"""
    contest_schema = convert_codeforces_contest_schema(
        get_contest_with_codeforces(contest_id)
    )
    return contest_schema


def add_contest(contest_id: int) -> ContestSchema:
    """add contest with contest_id"""

    contests_schema = get_contests(id=contest_id)

    if len(contests_schema) > 0:
        return contests_schema[0]

    contest_schema = get_contest_with_codeforces(contest_id)

    contest_schema = add_contest_with_schema(contest_schema)
    # TODO: rewrite problems get to event
    problems_schema = add_problems_with_cf(contest_id)
    contest_schema.problems = problems_schema

    return contest_schema


def update_contest_with_codeforces(contest_id: int) -> ContestSchema | None:
    contest_cf_schema = get_contest_with_codeforces(contest_id)

    if contest_cf_schema is None:
        return None

    contests_schema = get_contests(id=contest_id)
    if contests_schema == []:
        return None
    contest_schema = contests_schema[0]

    contest_schema = update_contest(
        contest_schema.id, **contest_cf_schema.model_dump())

    return contest_schema


def get_contest_table_rows(contest_id: int) -> list:
    # TODO: write tests
    rows = list()

    users = get_users()

    # TODO: rewrite, if user is contestant, but he has no submissions
    for user in users:
        submissions = get_submissions(contest_id=contest_id, author_id=user.id)
        if len(submissions):
            rows.append({"user": user, "submissions": submissions})

        teams = get_teams_with_handle_member(handle=user.handle)
        for team in teams:
            if team in (row.get("team", None) for row in rows):
                continue
            submissions = get_submissions(
                contest_id=contest_id, team_id=team.id)
            if len(submissions) == 0:
                continue
            rows.append({"team": team, "submissions": submissions})

    return rows


def delete_contest_and_deps(contest_id: int) -> ContestSchema:
    contest = delete_contest(contest_id)
    delete_submissions(contest_id=contest_id)
    delete_problems(contest_id=contest_id)
    return contest


def update_students_cf_submissions(handle: str, contest_id: int) -> list[SubmissionSchema]:
    submissions = convert_codeforces_submissions_schema(
        codeforces_contest.status(contestId=contest_id, handle=handle)
    )

    submissions_db = get_submissions(contest_id=contest_id)
    submissions_db_id = [
        submission.id
        for submission in submissions_db
    ]

    submissions_added = []

    for submission in submissions:
        if submission.id in submissions_db_id:
            update_submission(submission.id, **submission.model_dump())
        else:
            submission.author = get_user(handle=submission.author.handle)
            try:
                submission.problem = get_problems(
                    contest_id=submission.contest_id,
                    index=submission.problem.index
                )[0]
            except IndexError:
                logging.warning((f"IndexError. Try get problem with "
                                 f"{contest_id=} and "
                                 f"{submission.problem.index=}"
                                 f" from DB."))
            else:
                submissions_added.append(
                    add_submission_with_schema(submission)
                )

    submissions_added = [x for x in submissions_added if x]

    return submissions_added
