"""Application module."""

# pylint: disable=redefined-outer-name

from fastapi import FastAPI

from src.dependency_injection.di import Container
from src.entrypoints.rest.api import router


def create_app() -> FastAPI:
    """Creates FastAPI app and initilize resources"""

    container = Container()

    app = FastAPI()
    app.container = container
    app.container.init_resources()
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
