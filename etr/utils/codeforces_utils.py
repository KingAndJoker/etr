""" utils for work with Codeforces API """
import os

import requests

from etr.db import get_db
from etr.schemas.contest import ContestSchema


CODEFORCES_API_CONTEST_URL = "https://codeforces.com/api/contest.standings"


def get_contest(contest_id: int, *,
                as_manager: bool | None = None,
                from_: int | None = None,
                count: int | None = None,
                handles: list[str] | None = None,
                # room: int | str | None = None,
                show_unofficial: bool | None = None) -> ContestSchema | None:
    contest_url = f"{CODEFORCES_API_CONTEST_URL}?contestId={contest_id}"
    if as_manager:
        contest_url += f"&asManager={as_manager}"
    if from_:
        contest_url += f"&from={from_}"
    if count:
        contest_url += f"&{count = }"
    if handles:
        contest_url += f"&handles={';'.join(handles)}"
    if show_unofficial:
        contest_url += f"&showUnofficial={show_unofficial}"

    response = requests.get(contest_url)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as exp:
        print(exp.with_traceback())
        return None

    try:
        contest = ContestSchema(*response_json)
    except Exception as exp:
        print(exp.with_traceback)
        return None

    return contest
