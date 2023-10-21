"""run file"""
import os

from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv

from .models.base import Base


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    load_dotenv()
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
    )
    URL_PREFIX = os.getenv("URL_PREFIX", "")
    # app.config.from_file("pyproject.toml")

    # register the database commands
    from etr import db

    # Base.metadata.create_all(app.config["DATABASE_ENGINE"])
    db.init_db(app)

    # apply the blueprints to the app
    from etr.views import user
    from etr.views import index
    from etr.views import contest
    from etr.views import contest_status
    from etr.views.api import api_problem
    from etr.views.api import api_user
    from etr import rpc
    app.register_blueprint(index.bp, url_prefix=URL_PREFIX)
    app.register_blueprint(user.bp, url_prefix=URL_PREFIX + "/user")
    app.register_blueprint(contest.bp, url_prefix=URL_PREFIX + "/contest")
    app.register_blueprint(contest_status.bp, url_prefix=URL_PREFIX + "/status")
    app.register_blueprint(api_problem.bp, url_prefix=URL_PREFIX + "/api")
    app.register_blueprint(api_user.bp, url_prefix=URL_PREFIX + "/api")
    app.register_blueprint(rpc.bp, url_prefix=URL_PREFIX + "/rpc")

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index

    return app
