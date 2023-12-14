import os

from dotenv import load_dotenv

load_dotenv()

URL_PREFIX = os.getenv("URL_PREFIX", "")

DEFAULT_DATABASE_URL = "sqlite:///:memory:"
DATABASE_URL = os.getenv("URL_DATABASE", DEFAULT_DATABASE_URL)
SQLALCHEMY_ECHO = os.getenv("DATABASE_ECHO", "true").lower() == "true"
