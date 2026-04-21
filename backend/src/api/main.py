from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.response_handlers.install import install_handlers
from src.api.routers.analytics import router as analytics_router
from src.api.routers.auth import router as auth_router
from src.api.routers.banking import router as banking_router
from src.api.routers.categorization_rules import router as rules_router
from src.api.routers.categories import router as categories_router
from src.api.routers.health import router as health_router
from src.api.routers.users import router as users_router
from src.shared.env import Settings

API_PREFIX = "/api"


def create_app(allow_origins: list[str] | None = None) -> FastAPI:
    app = FastAPI(title="Pure Finance")
    if allow_origins is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    install_handlers(app)
    app.include_router(auth_router, prefix=API_PREFIX)
    app.include_router(users_router, prefix=API_PREFIX)
    app.include_router(analytics_router, prefix=API_PREFIX)
    app.include_router(banking_router, prefix=API_PREFIX)
    app.include_router(categories_router, prefix=API_PREFIX)
    app.include_router(rules_router, prefix=API_PREFIX)
    app.include_router(health_router, prefix=API_PREFIX)
    return app


def create_production_app() -> FastAPI:
    from src.shared.logging import configure_logging
    configure_logging()
    settings = Settings()
    return create_app(allow_origins=settings.cors_allowed_origins)
