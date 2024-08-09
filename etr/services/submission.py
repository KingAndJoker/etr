import time

from loguru import logger

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


@logger.catch(reraise=True)
def update_submissions_with_codeforces(
    contest_id: int,
) -> list[SubmissionSchema] | None:
    """функция обновляет решения для соревнования

    Args:
        contest_id (int): id соревнования

    Returns:
        list[SubmissionSchema] | None: список добавленных в базу данных посылок
    """
    logger.info(f"хочу обновить посылки для {contest_id=}")
    added_submissions = list()

    handles = [user.handle.lower() for user in get_users()]
    teams_id = [team.id for team in get_teams()]

    logger.debug(f"получаю посылки cf_subs_json")
    cf_subs_json = contest.status_json(contestId=contest_id)
    count_requests = 20
    delay_between_requests = 0.5
    while cf_subs_json is None and count_requests > 0:
        time.sleep(delay_between_requests)
        cf_subs_json = contest.status_json(contest_id)
        count_requests -= 1
    if cf_subs_json is None:
        logger.warning(f"не смог получить cf_subs_json")
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
        sub_is_exist = get_submission(id=submission.id)
        if sub_is_exist is not None:
            update_submission(sub_is_exist.id, **params)
        else:
            sub_add = add_submission_with_schema(submission)
            if sub_add is None:
                continue
            added_submissions.append(sub_add)

    logger.success(f"добавил {len(added_submissions)=} посылок")
    return added_submissions


def make_params_for_submission(submission: SubmissionSchema) -> dict:
    """функция преобразует SubmissionSchema и удаляет поле problem, author, team

    Args:
        submission (SubmissionSchema): посылка

    Returns:
        dict: словарь с результатом
    """
    params = submission.model_dump()

    if "problem" in params:
        params.pop("problem")
    if "author" in params:
        params.pop("author")
    if "team" in params:
        params.pop("team")

    return params


def update_submissions_for_user_with_codeforces(handle: str, start_with_unix: int = 0):
    """функция обновляет посылки для заданного пользователя

    Args:
        handle (str): handle пользователя
        start_with_unix (int, optional): с какого момента времени нас интересуют посылки. Defaults to 0.

    Returns:
        _type_: посылки пользователя
    """
    logger.info(f"хочу обновить посылку для {handle=}")
    codeforces_submissions = user_status(handle)
    if codeforces_submissions is None:
        logger.error(f"не смог получить посылки {handle=}")
        return []
    submissions = [
        submission
        for submission in convert_codeforces_submissions_schema(codeforces_submissions)
        if submission.creation_time_seconds > start_with_unix
    ]
    submissions_return: list[SubmissionSchema] = []

    contests = get_contests()
    contests_id = [contest.id for contest in contests]

    for submission in submissions:
        if submission.contest_id is None:
            break
        if submission.contest_id not in contests_id:
            event = ParseCodeforcesContestByContestId(submission.contest_id)
            results = handler(event)
            contests = get_contests()
            contests_id = [contest.id for contest in contests]

        sub_db = get_submission(id=submission.id)
        if sub_db:
            submissions_return.append(
                update_submission(
                    submission_id=sub_db.id, **submission.model_dump()
                )
            )
        else:
            submissions_return.append(add_submission_with_schema(submission))
    logger.success(f"добавил {len(submissions_return)=} решений пользователя")
    return submissions_return


@logger.catch(reraise=True)
def update_submissions_for_all_users_with_codeforces():
    """функция обновляет все посылки у всех пользователей

    Returns:
        _type_: возвращает все добавленные посылки
    """
    users = get_users(watch=True)
    if users is None:
        logger.warning("не смог получить из базы данных всех пользователей")
        return []
    submissions: list[SubmissionSchema] = []
    for user in users:
        logger.info(f"обновляю все посылки для {user.handle=}")
        submissions_of_user = []
        try:
            submissions_of_user.extend(update_submissions_for_user_with_codeforces(handle=user.handle))
        except Exception as err: # если возникнут проблемы с обновлением одного пользователя
            print(err)
        submissions.extend(submissions_of_user)
    logger.success(f"для {len(users)=} добавил {len(submissions)=} решений")
    return submissions
