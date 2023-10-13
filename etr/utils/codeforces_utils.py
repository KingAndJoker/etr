""" utils for work with Codeforces API """
import os

import requests

from etr.db import get_db
from etr.schemas.contest import ContestSchema
from etr.schemas.problem import ProblemSchema
from etr.schemas.submission import SubmissionSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema


CODEFORCES_API_CONTEST_URL = "https://codeforces.com/api/contest.standings"
CODEFROCES_API_SUBMISSION_URL = "https://codeforces.com/api/contest.status"
CODEFORCES_API_USER_INFO_URL = "https://codeforces.com/api/user.info"


def get_contest(contest_id: int, *,
                as_manager: bool | None = None,
                from_: int | None = None,
                count: int | None = None,
                handles: list[str] | None = None,
                # room: int | str | None = None,
                show_unofficial: bool | None = None,
                lang: str = "en") -> ContestSchema | None:
    contest_url = f"{CODEFORCES_API_CONTEST_URL}?" \
        f"contestId={contest_id}" \
        f"&lang={lang}"
    if as_manager:
        contest_url += f"&asManager={as_manager}"
    if from_:
        contest_url += f"&from={from_}"
    if count:
        contest_url += f"&{count =}"
    if handles:
        contest_url += f"&handles={';'.join(handles)}"
    if show_unofficial:
        contest_url += f"&showUnofficial={show_unofficial}"

    response = requests.get(contest_url)

    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp)
        return None

    contest: ContestSchema | None = None
    if response_json["status"] == "OK":
        try:
            contest = ContestSchema(**response_json["result"]["contest"])
        except Exception as exp:
            print(exp)

    return contest


def get_submission(
        contestId: int, *,
        as_manager: bool | None = None,
        handle: str | None = None,
        from_: int | None = None,
        count: int | None = None,
        lang: str = "en") -> list[SubmissionSchema] | None:
    submission_url = f"{CODEFROCES_API_SUBMISSION_URL}?" \
        f"contestId={contestId}" \
        f"&lang={lang}"
    if as_manager:
        submission_url += f"&asManager={as_manager}"
    if handle:
        submission_url += f"&handle={handle}"
    if from_:
        submission_url += f"&from={from_}"
    if count:
        submission_url += f"&{count = }"

    print(submission_url)

    submissions: list[SubmissionSchema] | None = None
    response = requests.get(submission_url)
    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except Exception as exp:
        print(exp)
        return None

    if response_json["status"] == "OK":
        for i, submission in enumerate(response_json["result"]):
            if "teamName" in response_json["result"][i]["author"]:
                team_users = [
                    UserSchema(handle=user["handle"])
                    for user in response_json["result"][i]["author"]["members"]
                ]
                response_json["result"][i]["author"] = TeamSchema(
                    **response_json["result"][i]["author"], users=team_users
                )

            else:
                response_json["result"][i]["author"] = UserSchema(
                    handle=submission["author"]["members"][0]["handle"]
                )

        submissions = [
            SubmissionSchema(**submission)
            for submission in response_json["result"]
        ]

    return submissions


def get_user(handle: str, lang: str = "en") -> UserSchema | None:
    user_url = f"{CODEFORCES_API_USER_INFO_URL}?handles={handle}&lang={lang}"

    response = requests.get(user_url)

    if response.status_code != 200:
        return None

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp)
        return None

    user: UserSchema | None = None
    if response_json["status"] == "OK":
        user = UserSchema(**response_json["result"][0])
    return user


def get_users(handles: list[str], lang: str = "en") -> list[UserSchema | None]:
    users: list[UserSchema | None] = [
        get_user(handle, lang=lang)
        for handle in handles
    ]
    return users


def get_problem_with_contest(contest_id: int, *, lang: str = "en") -> list[ProblemSchema] | None:
    problem_url = f"{CODEFORCES_API_CONTEST_URL}?" \
        f"contestId={contest_id}" \
        f"&lang={lang}"

    print(f"{problem_url=}")
    response = requests.get(problem_url)
    if response.status_code != 200:
        print(1)
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
        ProblemSchema(**problem)
        for problem in response_json["result"]["problems"]
    ]

    return problems
