"""contest status handler"""
import requests
from flask import Blueprint, render_template

from codeforces_2BIWY.db import get_db
from codeforces_2BIWY.models.contest import Contest
from codeforces_2BIWY.models.user import User
from codeforces_2BIWY.schemas.contest import ContestSchema
from codeforces_2BIWY.schemas.user import UserSchema
from codeforces_2BIWY.schemas.submission import SubmissionSchema


bp = Blueprint("contest_status", __name__, url_prefix="/status")


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
                f"&handle={user.handler}"
            )
            response_json = response.json()

            if response_json["status"] == "OK":
                for i, status in enumerate(response_json["result"]):
                    response_json["result"][i]["author"] = user

                statuses += [
                    SubmissionSchema(**data) for data in response_json["result"]
                ]

    return render_template("status.html", statuses=statuses)
