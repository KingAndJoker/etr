""" utils for work with Codeforces API """
import requests

from etr.library.codeforces.utils.generate_url import generate_url
from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.user import CodeforcesUserSchema
from etr.library.codeforces.schemas.team import CodeforcesTeamSchema


def get_contest(
    contest_id: int,
    *,
    as_manager: bool | None = None,
    from_: int | None = None,
    count: int | None = None,
    handles: list[str] | None = None,
    room: int | str | None = None,
    show_unofficial: bool | None = None,
    lang: str = "en",
) -> CodeforcesContestSchema | None:
    if handles is not None:
        handles = ";".join(handles)

    contest_url = generate_url(
        "contest.standings",
        contestId=contest_id,
        asManager=as_manager,
        from_=from_,
        count=count,
        handles=handles,
        room=room,
        showUnofficial=show_unofficial,
        lang=lang,
    )

    response = requests.get(contest_url)

    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp)
        return None

    contest: CodeforcesContestSchema | None = None
    if response_json["status"] == "OK":
        try:
            print(response_json["result"]["problems"])
            contest = CodeforcesContestSchema(**response_json["result"]["contest"])
            contest.problems = [
                CodeforcesProblemSchema(**problem)
                for problem in response_json["result"]["problems"]
            ]
        except Exception as exp:
            print(exp)

    return contest


def get_submission(
    contestId: int,
    *,
    as_manager: bool | None = None,
    handle: str | None = None,
    from_: int | None = None,
    count: int | None = None,
    lang: str = "en",
) -> list[CodeforcesSubmissionSchema] | None:
    submission_url = generate_url(
        "contest.status",
        contestId=contestId,
        asManager=as_manager,
        handle=handle,
        from_=from_,
        count=count,
        lang=lang,
    )

    submissions: list[CodeforcesSubmissionSchema] | None = None

    # TODO: rewrite logger
    print(f"get submission")
    print(f"{submission_url=}")

    response = requests.get(submission_url)
    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except Exception as exp:
        print(exp)
        return None

    if response_json["status"] == "OK":
        print(f"length submissions answer: {len(response_json['result'])}")

        for i, submission in enumerate(response_json["result"]):
            response_json["result"][i]["type_of_member"] = submission["author"][
                "participantType"
            ]
            if "teamName" in response_json["result"][i]["author"]:
                team_users = [
                    CodeforcesUserSchema(handle=user["handle"])
                    for user in response_json["result"][i]["author"]["members"]
                ]
                response_json["result"][i]["author"] = CodeforcesTeamSchema(
                    **response_json["result"][i]["author"], users=team_users
                )

            else:
                response_json["result"][i]["author"] = CodeforcesUserSchema(
                    handle=submission["author"]["members"][0]["handle"]
                )

        submissions = [
            CodeforcesSubmissionSchema(**submission)
            for submission in response_json["result"]
        ]

    return submissions


def get_user(handle: str, lang: str = "en") -> CodeforcesUserSchema | None:
    user_url = generate_url("user.info", handles=handle, lang=lang)

    response = requests.get(user_url)

    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp)
        return None

    user: CodeforcesUserSchema | None = None
    if response_json["status"] == "OK":
        user = CodeforcesUserSchema(**response_json["result"][0])
    return user


def get_users(
    handles: list[str], lang: str = "en"
) -> list[CodeforcesUserSchema | None]:
    users: list[CodeforcesUserSchema | None] = [
        get_user(handle, lang=lang) for handle in handles
    ]
    return users


def get_problem_with_contest(
    contest_id: int, *, lang: str = "en"
) -> list[CodeforcesProblemSchema] | None:
    problem_url = generate_url(
        "contest.standings", contestId=contest_id, from_=1, count=1, lang=lang
    )

    response = requests.get(problem_url)
    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp)
        return None

    if response_json["status"] != "OK":
        print(2)
        return None

    problems = [
        CodeforcesProblemSchema(**problem)
        for problem in response_json["result"]["problems"]
    ]

    return problems
