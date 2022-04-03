from typing import Callable
from fastapi import FastAPI

from app.databases.tasks import connect_to_db, close_db_connection


def start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        connect_to_db(app)

    return start_app


def stop_app_handler(app: FastAPI) -> Callable:
    def stop_app() -> None:
        close_db_connection(app)

    return stop_app
