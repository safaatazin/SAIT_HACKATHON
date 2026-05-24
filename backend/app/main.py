from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import ask, events, upload_frame


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="LastSeen API",
        description="AI Object Memory Room Scanner backend",
        version="0.1.0",
    )

    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins != ["*"] else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(upload_frame.router, prefix="/api")
    app.include_router(ask.router, prefix="/api")
    app.include_router(events.router, prefix="/api")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
