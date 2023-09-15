"""contest views"""
import requests
from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from codeforces_2BIWY.db import get_db
from codeforces_2BIWY.models.contest import Contest
from codeforces_2BIWY.schemas.contest import ContestSchema


bp = Blueprint("contest", __name__, url_prefix="/contest")


@bp.route("/")
def get_contests():
    contests = None
    with get_db() as session:
        contests = session.query(Contest).all()
        contests = [
            ContestSchema.model_validate(contest)
            for contest in contests
        ]

    return render_template("contests.html", contests=contests)


@bp.route("/new", methods=["GET", "POST"])
def new_contest():
    if request.method == "GET":
        return render_template("new_contest.html")

    elif request.method == "POST":
        contest_id = request.form.get("contest-id")
        response = requests.get(
            f"https://codeforces.com/api/contest.standings?"
            f"contestId={contest_id}"
            f"&count=1"
        )
        response_json = response.json()

        if response_json['status'] == "OK":
            with get_db() as session:
                contest = Contest(**response_json["result"]["contest"])
                session.add(contest)
                session.commit()
        return redirect("/")
