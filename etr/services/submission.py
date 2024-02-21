import time

from etr.schemas.submission import SubmissionSchema
from etr.crud.user import get_user
from etr.crud.user import get_users
from etr.crud.team import get_teams
from etr.crud.team import add_team_with_schema
from etr.crud.team import is_our_team_json
from etr.crud.submission import is_our_submission
from etr.crud.submission import add_submission_with_schema
from etr.crud.submission import get_submission
from etr.crud.submission import update_submission
from etr.crud.contest import get_contests
from etr.events.contest import ParseCodeforcesContestByContestId
from etr.handlers import handler
from etr.library.codeforces import contest
from etr.library.codeforces.user import status as user_status
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema
from etr.utils.services.contest import parse_url
from etr.utils.codeforces.convert import convert_codeforces_submission_schema
from etr.utils.codeforces.convert import convert_codeforces_submissions_schema
from etr.utils.codeforces.convert import convert_codeforces_team_schema


def update_submissions_with_codeforces(
    contest_id: int,
) -> list[SubmissionSchema] | None:
    added_submissions = list()

    handles = [user.handle.lower() for user in get_users()]
    teams_id = [team.id for team in get_teams()]

    cf_subs_json = contest.status_json(contestId=contest_id)
    count_requests = 20
    delay_between_requests = 0.5
    while cf_subs_json is None and count_requests > 0:
        time.sleep(delay_between_requests)
        cf_subs_json = contest.status_json(contest_id)
        count_requests -= 1
    if cf_subs_json is None:
        return None

    for submission_json in cf_subs_json:
        if (
            "teamId" in submission_json["author"]
            and submission_json["author"]["teamId"] not in teams_id
            and is_our_team_json(submission_json["author"])
        ):
            team = add_team_with_schema(
                convert_codeforces_team_schema(
                    CodeforcesTeamSchema(**submission_json["author"])
                )
            )
            teams_id.append(team.id)
        if not is_our_submission(submission_json, handles, teams_id):
            continue
        submission = convert_codeforces_submission_schema(
            CodeforcesSubmissionSchema(**submission_json)
        )
        submission.type_of_member = submission_json["author"]["participantType"]
        if submission is None:
            continue
        params = make_params_for_submission(submission)
        sub_is_exist = get_submission(**params)
        if sub_is_exist is not None:
            update_submission(sub_is_exist.id, **params)
        else:
            sub_add = add_submission_with_schema(submission)
            if sub_add is None:
                continue
            added_submissions.append(sub_add)

    return added_submissions


def make_params_for_submission(submission: SubmissionSchema) -> dict:
    params = submission.model_dump()

    if "problem" in params:
        params.pop("problem")
    if "author" in params:
        params.pop("author")

    return params


def update_submissions_for_user_with_codeforces(handle: str, start_with_unix: int = 0):
    submissions = [
        submission
        for submission in convert_codeforces_submissions_schema(user_status(handle))
        if submission.creation_time_seconds > start_with_unix
    ]
    submissions_return: list[SubmissionSchema] = []

    contests = get_contests()
    contests_id = [contest.id for contest in contests]

    for submission in submissions:
        if submission.contest_id not in contests_id:
            event = ParseCodeforcesContestByContestId(submission.contest_id)
            results = handler(event)
            contests = get_contests()
            contests_id = [contest.id for contest in contests]

        sub_db = get_submission(id=submission.id)
        if sub_db:
            submissions_return.append(update_submission(submission_id=sub_db.id, **submission.model_dump()))
        else:
            submissions_return.append(add_submission_with_schema(submission))
    return submissions_return
