"""contest views"""
from flask import (
    Blueprint,
    render_template
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
