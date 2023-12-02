"""contest views"""
import requests
from flask import (
    Blueprint,
    render_template,
    request,
    redirect
)

from etr.db import get_db
from etr.models.contest import Contest
from etr.schemas.contest import ContestSchema
from etr.events.contest import ParseContestBeforeUpdate
from etr.handlers import handle
from etr.utils.services.contest import parse_url


bp = Blueprint("contest", __name__)


@bp.route("/")
def get_contests():
    return render_template("contests.html")


@bp.route("/new", methods=["GET", "POST"])
def new_contest():
    if request.method == "GET":
        return render_template("new_contest.html")

    elif request.method == "POST":
        contest_url = request.form.get("contest-url")

        url = parse_url(contest_url)
        event = ParseContestBeforeUpdate(url)
        results = handle(event)

        return redirect("/etr")


@bp.route("/<contest_id>")
def get_contest(contest_id: int):
    with get_db() as session:
        contest_db: Contest = session.query(Contest).filter(
            Contest.id == contest_id).\
            one_or_none()

        contest = ContestSchema.model_validate(contest_db)

    return render_template("contest.html", contest=contest)
