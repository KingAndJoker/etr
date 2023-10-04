"""contest status handler"""
import time

import requests
from flask import Blueprint, render_template

from etr.db import get_db
from etr.models.contest import Contest
from etr.models.user import User
from etr.schemas.contest import ContestSchema
from etr.schemas.user import UserSchema
from etr.schemas.team import TeamSchema
from etr.schemas.submission import SubmissionSchema


bp = Blueprint("contest_status", __name__)


@bp.route("/")
def status():
    contests = None
    users = None

    with get_db() as session:
        contests = session.query(Contest).all()
        users = session.query(User).all()

    contests = [ContestSchema.model_validate(contest) for contest in contests]
    users = [UserSchema.model_validate(user) for user in users]

    statuses = list()

    for contest in contests:
        for user in users:
            response = requests.get(
                f"https://codeforces.com/api/contest.status?"
                f"contestId={contest.id}"
                f"&handle={user.handle}"
            )
            time.sleep(2)

            if response.status_code != 200:
                return render_template("status.html")
            try:
                response_json = response.json()
            except:
                response_json = {"status": "zxc"}

            if response_json["status"] == "OK":
                for data in response_json["result"]:
                    author = None
                    if "teamId" in data["author"]:
                        author = TeamSchema(
                            id=data["author"]["teamId"],
                            teamName=data["author"]["teamName"],
                            users=[
                                UserSchema(**user_data)
                                for user_data in data["author"]["members"]
                            ]
                        )
                    else:
                        author = UserSchema(**data["author"]["members"][0])
                    del data["author"]

                    statuses += [SubmissionSchema(**data, author=author)]

    return render_template("status.html", statuses=statuses)