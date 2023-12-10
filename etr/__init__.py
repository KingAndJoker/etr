"""run file"""
import os

# from flask import Flask
from fastapi import FastAPI
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import Engine

from .config import config, Config


def create_app(**kwargs):
    """Create and configure an instance of the Flask application."""

    config = Config(**kwargs)

    app = FastAPI(
        docs_url=config.URL_PREFIX + "/docs",
        redoc_url=config.URL_PREFIX + "/redoc",
    )
    from etr.api import api_user
    from etr.api import api_submission
    from etr.api import api_problem
    from etr.api import api_contest
    app.include_router(
        api_user.router,
        prefix=f"{config.URL_PREFIX}/api",
        tags=["api"]
    )
    app.include_router(
        api_submission.router,
        prefix=f"{config.URL_PREFIX}/api",
        tags=["api"]
    )
    app.include_router(
        api_problem.router,
        prefix=f"{config.URL_PREFIX}/api",
        tags=["api"]
    )
    app.include_router(
        api_contest.router,
        prefix=f"{config.URL_PREFIX}/api",
        tags=["api"]
    )

    from etr import rpc
    app.include_router(
        rpc.router,
        prefix=f"{config.URL_PREFIX}/rpc",
        tags=["rpc"],
    )

    from etr.views import user as user_view
    app.include_router(
        user_view.router,
        prefix=f"{config.URL_PREFIX}"
    )

    # from etr.views import user
    # from etr.views import index
    # from etr.views import contest
    # from etr.views import contest_status

    # app.register_blueprint(index.bp, url_prefix=URL_PREFIX)
    # app.register_blueprint(user.bp, url_prefix=URL_PREFIX + "/user")
    # app.register_blueprint(contest.bp, url_prefix=URL_PREFIX + "/contest")
    # app.register_blueprint(
    #     contest_status.bp,
    #     url_prefix=URL_PREFIX + "/status"
    # )

    return app


app = create_app()
