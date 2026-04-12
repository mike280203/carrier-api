"""Main-App fuer eine saubere Carrier-Grundstruktur."""

from contextlib import asynccontextmanager
from time import time
from typing import Final

from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

from carrier.banner import banner
from carrier.config import dev_db_populate, dev_keycloak_populate
from carrier.config.dev.db_populate import db_populate
from carrier.config.dev.db_populate_router import router as db_populate_router
from carrier.config.dev.keycloak_populate import keycloak_populate
from carrier.config.dev.keycloak_populate_router import (
    router as keycloak_populate_router,
)
from carrier.repository import engine
from carrier.router.carrier_router import router as carrier_router
from carrier.router.carrier_write_router import router as carrier_write_router


class CarrierResponse(BaseModel):
    """API-Response fuer einen Carrier."""

    id: int
    name: str
    nation: str
    carrier_type: str


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: RUF029
    """Optionale Dev-Initialisierung und sauberes Shutdown."""
    if dev_db_populate:
        db_populate()
    if dev_keycloak_populate:
        keycloak_populate()
    banner(app.routes)
    yield
    logger.info("Der Server wird heruntergefahren")
    engine.dispose()


app: Final = FastAPI(
    title="Carrier API",
    description="Saubere Basis fuer ein FastAPI-Projekt mit PostgreSQL und SQLAlchemy.",
    version="0.1.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)
app.add_middleware(GZipMiddleware, minimum_size=500)


@app.middleware("http")
async def log_request_and_timing(request: Request, call_next) -> Response:
    """Request und Antwortdauer protokollieren."""
    logger.debug("{} '{}'", request.method, request.url)
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000
    logger.debug(
        "Response time: {:.2f} ms, statuscode: {}",
        duration_ms,
        response.status_code,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.get("/")
def root() -> dict[str, str]:
    """Einfacher Startpunkt fuer Smoke-Tests."""
    return {"message": "Carrier API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    """Health-Endpunkt fuer lokale Checks und Docker."""
    return {"status": "ok"}


app.include_router(carrier_router)
app.include_router(carrier_write_router)


if dev_db_populate:
    app.include_router(db_populate_router, prefix="/dev")
if dev_keycloak_populate:
    app.include_router(keycloak_populate_router, prefix="/dev")
