import os

from dotenv import load_dotenv
from sqlalchemy import Engine

from .db import init_db


load_dotenv()

# TODO: https://fastapi.tiangolo.com/advanced/settings/
class Config():
    URL_PREFIX: str
    DATABASE_URL: str
    SQLALCHEMY_ECHO: bool
    engine: Engine

    def __init__(
            self,
            URL_PREFIX: str | None = None,
            DATABASE_URL: str | None = None,
            SQLALCHEMY_ECHO: bool | None = None,
            **kwargs
    ) -> None:
        self.URL_PREFIX = URL_PREFIX or os.getenv("URL_PREFIX", "")

        DEFAULT_DATABASE_URL = "sqlite:///:memory:"
        self.DATABASE_URL = DATABASE_URL or \
            os.getenv("URL_DATABASE", DEFAULT_DATABASE_URL)

        self.SQLALCHEMY_ECHO = SQLALCHEMY_ECHO or \
            os.getenv("DATABASE_ECHO", "true").lower() == "true"

        self.engine = init_db(self.DATABASE_URL, self.SQLALCHEMY_ECHO)


config = None
