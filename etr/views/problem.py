from flask import Blueprint, render_template

bp = Blueprint("problem", __name__)


@bp.get("/")
def problems():
    """return problems.html template"""
    return render_template("problems.html")
