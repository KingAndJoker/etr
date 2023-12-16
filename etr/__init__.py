"""run file"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from etr import config
from etr import db


# TODO: https://fastapi.tiangolo.com/advanced/settings/
def create_app():
    """Create and configure an instance of the FastAPI application."""

    db.init_db(engine=db.engine)

    app = FastAPI(
        openapi_url=config.URL_PREFIX + "/openapi.json",
        docs_url=config.URL_PREFIX + "/docs",
        redoc_url=config.URL_PREFIX + "/redoc",
    )
    app.mount(
        f"{config.URL_PREFIX}/static",
        StaticFiles(directory="etr/static"),
        name="static",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from etr.api import api_user
    from etr.api import api_submission
    from etr.api import api_problem
    from etr.api import api_contest

    app.include_router(api_user.router, prefix=f"{config.URL_PREFIX}/api", tags=["api"])
    app.include_router(
        api_submission.router, prefix=f"{config.URL_PREFIX}/api", tags=["api"]
    )
    app.include_router(
        api_problem.router, prefix=f"{config.URL_PREFIX}/api", tags=["api"]
    )
    app.include_router(
        api_contest.router, prefix=f"{config.URL_PREFIX}/api", tags=["api"]
    )

    from etr import rpc

    app.include_router(
        rpc.router,
        prefix=f"{config.URL_PREFIX}/rpc",
        tags=["rpc"],
    )

    from etr.views import user as user_view
    from etr.views import index as index_view
    from etr.views import contest as contest_view
    from etr.views import problem as problem_view

    app.include_router(contest_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(index_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(user_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(problem_view.router, prefix=f"{config.URL_PREFIX}")

    return app


app = create_app()
