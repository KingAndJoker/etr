"""run file"""
import os

from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import Engine

from .models.base import Base


load_dotenv()

URL_PREFIX = os.getenv("URL_PREFIX", "")
DEFAULT_DATABASE_URL = "sqlite:///storage/users.db"
DATABASE_URL = os.getenv("URL_DATABASE", DEFAULT_DATABASE_URL)
ECHO = os.getenv("DATABASE_ECHO", "True") in ("true", "True")


def create_app(engine: Engine | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True,
                static_url_path=f"{URL_PREFIX}/static")

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if engine is None:
        from etr import db

        engine = db.init_db(DATABASE_URL, ECHO)
    app.config["engine"] = engine

    from etr.views import user
    from etr.views import index
    from etr.views import contest
    from etr.views import contest_status
    from etr.api import api_problem
    from etr.api import api_user
    from etr.api import api_submission
    from etr import rpc
    app.register_blueprint(index.bp, url_prefix=URL_PREFIX)
    app.register_blueprint(user.bp, url_prefix=URL_PREFIX + "/user")
    app.register_blueprint(contest.bp, url_prefix=URL_PREFIX + "/contest")
    app.register_blueprint(
        contest_status.bp, url_prefix=URL_PREFIX + "/status")
    app.register_blueprint(api_problem.bp, url_prefix=URL_PREFIX + "/api")
    app.register_blueprint(api_user.bp, url_prefix=URL_PREFIX + "/api")
    app.register_blueprint(api_submission.bp, url_prefix=URL_PREFIX + "/api")
    app.register_blueprint(rpc.bp, url_prefix=URL_PREFIX + "/rpc")

    return app
