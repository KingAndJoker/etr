"""
Script extract results from Codeforces API by timer.
Doc with API https://codeforces.com/apiHelp/methods#contest.status
"""
import time
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from codeforces_2BIWY.models.user import User
from codeforces_2BIWY.models.team import teams_users, Team
from codeforces_2BIWY.models.contest import Contest
from codeforces_2BIWY.models.submission import Submission
from codeforces_2BIWY.models.problem import Problem
from codeforces_2BIWY.db import get_db


def parse_result(results: list[dict], user: User) -> list[Submission]:
    """ parse results and return list of Submission """
    # TODO: https://github.com/users/KingAndJoker/projects/2?pane=issue&itemId=39579004

    submissions: list[Submission] = list()
    with get_db() as session:
        for result in results:
            submission = session.query(Submission).filter(Submission.id == result["id"])
            if submission is None:
                problem = Problem(**result["problem"])
                Submission(**result, author_id=user.id, problem=problem)
                
            submissions += [submission]

    return submissions


if __name__ == "__main__":
    FREQUENCY_PULL = 3600  # in seconds

    while True:
        with get_db() as session:
            users = session.query(User).all()
            contests = session.query(Contest).all()

            for user in users:
                for contest in contests:
                    url = f"https://codeforces.com/api/contest.status?" \
                          f"contestId={contest.id}&" \
                          f"handle={user.handle}"

                    response = requests.get(url)
                    try:
                        response_json = response.json()
                    except requests.exceptions.JSONDecodeError:
                        continue
                    time.sleep(2)

                    if response_json["status"] == "OK":
                        submissions = parse_result(
                            response_json["result"], user)
                        session.add_all(submissions)

            session.commit()

        time.sleep(FREQUENCY_PULL)
