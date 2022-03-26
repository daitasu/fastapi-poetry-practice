from fastapi import FastAPI

import app.models as models
from app.database import SessionLocal, engine
from app.api.routes import router as api_router

models.Base.metadata.create_all(bind=engine)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$ksGbpKo4SEVeYQImKWUYKubqqL/9B28E.ldD/u8Ed770w2rEquXy2",
        "disabled": False,
    }
}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_application():
    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    return app


app = get_application()
