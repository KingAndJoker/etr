import requests

from etr.library.codeforces.schemas.submission import CodeforcesSubmissionSchema
from etr.library.codeforces.utils.generate_url import generate_url
from etr.utils.request import Request


def status(handle: str,
           *,
           from_: int | None = None,
           count: int | None = None) -> list[CodeforcesSubmissionSchema] | None:
    """метод возвращает посылки пользователя

    https://codeforces.com/apiHelp/methods#user.status

    Args:
        handle (str): хендл пользователя
        from_ (int | None, optional): начиная с какой попытки. Defaults to None.
        count (int | None, optional): количество попыток. Defaults to None.

    Returns:
        list[CodeforcesSubmissionSchema] | None: список посылок пользователя
    """
    params = {
        key: value
        for key, value in {
            "handle": handle,
            "from": from_,
            "count": count
        }.items()
        if value is not None
    }
    url = generate_url("user.status", **params)
    request = Request()
    response = request.handle(url, "GET")
    if response.status_code != 200:
        return None

    data = response.json()
    if data["status"] != "OK":
        return None

    submissions = []
    for submission_data in data["result"]:
        submission = CodeforcesSubmissionSchema(
            **submission_data,
            participantType=submission_data["author"]["participantType"]
        )
        submissions.append(submission)

    return submissions
