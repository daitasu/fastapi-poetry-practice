from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_recycle=10)


def get_db_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_to_db(app: FastAPI) -> None:
    engine = create_engine(DATABASE_URL, pool_recycle=10)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        app.state._session = Session()
        print("--- DATABASE CONNECTION SUCCESS ---")
    except Exception as e:
        print("--- DATABASE CONNECTION ERROR ---")
        print(e)
        print("--- DATABASE CONNECTION ERROR ---")


def close_db_connection(app: FastAPI) -> None:
    try:
        app.state._session.close()
        print("--- DATABASE DISCONNECT SUCCESS ---")
    except Exception as e:
        print("--- DATABASE DISCONNECT ERROR ---")
        print(e)
        print("--- DATABASE DISCONNECT ERROR ---")
