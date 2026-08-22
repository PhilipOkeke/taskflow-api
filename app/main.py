"""TaskFlow API application factory and ASGI entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.auth_routes import router as auth_router
from app.config import Settings, get_settings
from app.database import build_engine
from app.routes import router as task_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a configured FastAPI application."""

    active_settings = settings or get_settings()
    engine = build_engine(active_settings.database_url)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        SQLModel.metadata.create_all(engine)
        yield
        engine.dispose()

    application = FastAPI(
        title=active_settings.app_name,
        version=active_settings.app_version,
        description=(
            "A multi-user task management API with JWT authentication, "
            "database persistence, automated tests, and continuous integration."
        ),
        lifespan=lifespan,
    )
    application.state.engine = engine
    application.state.settings = active_settings
    application.include_router(auth_router)
    application.include_router(task_router)

    @application.get("/", tags=["service"])
    def service_info() -> dict[str, str]:
        return {
            "name": active_settings.app_name,
            "version": active_settings.app_version,
            "documentation": "/docs",
            "health": "/health",
        }

    @application.get("/health", tags=["service"])
    def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    return application


app = create_app()
