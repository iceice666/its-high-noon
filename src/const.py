import os
from logging import getLogger
from typing import TypeVar

from dotenv import load_dotenv
from quart import Quart
from quart.logging import default_handler

from src import scheduler
from src.database.question import QuestionsManager
from src.database.user import UsersManager
from src.i18n import I18nManager
from src.logger import setup_logger

T = TypeVar("T")

load_dotenv()


def get_env(key: str) -> str | None:
    return os.getenv(key)


def get_env_or_exit(key: str) -> str:
    r = os.getenv(key)
    if r is None:
        raise RuntimeError(f"Environment variable {key} not set")
    else:
        return r


def get_env_or_default(key: str, default: T) -> T:
    r = os.getenv(key)
    if r is None:
        return default
    else:
        return r



LINE_CHANNEL_SECRET = get_env_or_exit("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = get_env_or_exit("LINE_CHANNEL_ACCESS_TOKEN")

DB_NAME = get_env_or_exit("DB_NAME")
DB_PORT = get_env_or_default("DB_PORT", 5432)
DB_USER = get_env_or_exit("DB_USER")
DB_HOST = get_env_or_default("DB_HOST", "localhost")
DB_PASSWORD = get_env_or_exit("DB_PASSWORD")

QUESTIONS_DATABASE = QuestionsManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
USERS_DATABASE = UsersManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

setup_logger()

NAME = "It's high noon"

APP = Quart(NAME)
getLogger(APP.name).removeHandler(default_handler)

SCHEDULER = scheduler.Scheduler()

I18N = I18nManager()
