from etr.schemas.user import UserSchema
from etr.schemas.contest import ContestSchema
from etr.schemas.team import TeamSchema
from etr.crud.submission import get_submissions
from etr.crud.team import get_teams
from etr.crud.contest import get_contests
from etr.crud.user import get_user, get_users, add_user, update_user
from etr.library.codeforces.codeforces_utils import get_user as get_codeforces_user
from etr.library.dl_gsu_by_codeforces.parse_students import get_students
from etr.utils.codeforces.convert import convert_codeforces_user_schema
from etr.utils.dl_gsu_by_codeforces.convert import convert_dl_to_etr


def sync_user_with_dl():
    sync_users_schema = convert_dl_to_etr(get_students())

    users_schema = get_users()
    for dl_user in sync_users_schema:
        if dl_user.handle in (user_schema.handle for user_schema in users_schema):
            update_user_schema = get_user(
                handle=dl_user.handle
            )
            params = {
                key: value
                for key, value in dl_user.model_dump(exclude=("id")).items() if value is not None
            }
            update_user(update_user_schema.id, **params)
        else:
            add_user(dl_user)


def add_user_from_codeforces(handle: str, lang: str = "ru") -> UserSchema | None:
    user_schema = convert_codeforces_user_schema(
        get_codeforces_user(handle, lang=lang)
    )
    return add_user(user_schema)


def update_user_info_from_codeforces(handle: str) -> UserSchema | None:
    user_new = convert_codeforces_user_schema(
        get_codeforces_user(handle, lang="ru")
    )
    if user_new is None:
        return None

    user_etr = get_user(handle=handle)
    if user_etr is None:
        return None

    params = {
        key: value
        for key, value in user_new.model_dump(exclude=("id")).items() if value is not None
    }
    return_user = update_user(user_etr.id, **params)
    return return_user


def get_user_teams_by_handle(handle: str) -> list[TeamSchema]:
    return [
        team
        for team in get_teams()
        if handle in [
            user.handle
            for user in team.users
        ]
    ]


def get_user_contests(handle: str) -> list[ContestSchema]:
    user = get_user(handle)
    teams = get_user_teams_by_handle(handle)
    submissions = get_submissions(author_id=user.id)

    for team in teams:
        submissions += get_submissions(team_id=team.id)
    
    contests_id = list(
        set([submission.contest_id for submission in submissions])
    )

    contests = [
        contest
        for contest in get_contests()
        if contest.id in contests_id
    ]
    return contests
