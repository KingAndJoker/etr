"""run file"""
import time
import logging
from threading import Thread

from loguru import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from etr import config
from etr import db
from etr.services.submission import update_submissions_for_all_users_with_codeforces
from etr.services.problem import update_missing_tags_for_problems
from etr.services.problem import update_solved_count
from etr.services.recommendation import create_recommendations


logger.add(
    "logs/debug.log",
    format="{time} {level} {process} {thread} {function} {message}",
    level="DEBUG",
    catch=True,
    backtrace=True,
    rotation="1 week"
)
logger.add(
    "logs/debug.json",
    format="{time} {level} {process} {thread} {function} {message}",
    level="DEBUG",
    serialize=True,
    catch=True,
    rotation="1 week"
)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        loguru_logger = logger.opt(depth=0, exception=record.exc_info)
        loguru_logger.log(record.levelname, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0)


@logger.catch(reraise=True)
def autoupdate_info():
    while True:
        try:
            logger.info("circle of samsara: start auto update info")
            update_submissions_for_all_users_with_codeforces()
            update_missing_tags_for_problems()
            update_solved_count()
            create_recommendations()
            logger.info("circle of samsara: end")
        except Exception as exp:
            print(exp)
            logger.exception("circle of samsara: exception")


# TODO: https://fastapi.tiangolo.com/advanced/settings/
@logger.catch(reraise=True)
def create_app():
    """Create and configure an instance of the FastAPI application."""

    logger.debug("инициализируем базу данных")
    db.init_db(engine=db.engine)

    logger.debug("создаем экземпляр приложения")
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

    logger.debug("импортируем и подключаем все router")
    from etr.api import api_user
    from etr.api import api_submission
    from etr.api import api_problem
    from etr.api import api_contest
    from etr.api import api_recommendation

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
    app.include_router(
        api_recommendation.router, prefix=f"{config.URL_PREFIX}/api", tags=["api"]
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
    from etr.views import protocol as protocol_view
    from etr.views import recommendation as recommendation_view

    app.include_router(contest_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(index_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(user_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(problem_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(protocol_view.router, prefix=f"{config.URL_PREFIX}")
    app.include_router(recommendation_view.router, prefix=f"{config.URL_PREFIX}")

    if not config.DEBUG:
        logger.debug("создаем поток для авто подгрузки данных")
        Thread(
            target=autoupdate_info,
        ).start()

    return app


app = create_app()
