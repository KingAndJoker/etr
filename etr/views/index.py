"""index views"""
from flask import (
    Blueprint,
    render_template
)


bp = Blueprint("index", __name__)


@bp.get("/")
def index():
    """index page"""
    return render_template("index.html")


@bp.get("/about")
def about():
    """about page"""
    return render_template("about.html")


@bp.get("/api")
def api():
    """api page"""
    return render_template("api.html")
