import requests

from etr.library.codeforces.schemas.contest import CodeforcesContestSchema
from etr.library.codeforces.schemas.problem import CodeforcesProblemSchema
from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.schemas.ranklist_row import CodeforcesRanklistRowSchema
from etr.library.codeforces.utils.generate_url import generate_url


def standings(contest_id: int,
              as_manager: bool | None = None,
              from_: int | None = None,
              count: int | None = None,
              handles: str | None = None,
              room: int | None = None,
              show_unofficial: bool | None = None,
              lang: str = "ru") -> tuple[CodeforcesContestSchema, list[CodeforcesProblemSchema], CodeforcesRanklistRowSchema]:
    pass


def status(contestId: int, *,
           asManager: bool | None = None,
           handle: str | None = None,
           from_: int | None = None,
           count: int | None = None,
           lang: str = "ru") -> list[CodeforcesSubmissionSchema] | None:
    kwargs = {
        "contestId": contestId,
        "asManager": asManager,
        "handle": handle,
        "from": from_,
        "count": count,
        "lang": lang
    }
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    contest_status_url = generate_url(
        "contest.status",
        **kwargs
    )
    response = requests.get(contest_status_url)

    if response.status_code != 200:
        return None

    data = response.json()
    if data["status"] != "OK":
        return None

    submissions = []
    for submission_data in data["result"]:
        submission = CodeforcesSubmissionSchema(**submission_data)
        submissions.append(submission)

    return submissions


def status_json(contestId: int, *,
                asManager: bool | None = None,
                handle: str | None = None,
                from_: int | None = None,
                count: int | None = None,
                lang: str = "ru") -> list[dict] | None:
    kwargs = {
        "contestId": contestId,
        "asManager": asManager,
        "handle": handle,
        "from": from_,
        "count": count,
        "lang": lang
    }
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    contest_status_url = generate_url(
        "contest.status",
        **kwargs
    )
    response = requests.get(contest_status_url)

    if response.status_code != 200:
        return None

    data = response.json()
    if data["status"] != "OK":
        return None

    return data["result"]
