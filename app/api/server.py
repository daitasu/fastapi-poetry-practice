from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core import event_handler


def get_application():
    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    app.add_event_handler("startup", event_handler.start_app_handler(app))
    app.add_event_handler("shutdown", event_handler.stop_app_handler(app))

    return app


app = get_application()
