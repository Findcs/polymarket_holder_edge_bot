from fastapi import FastAPI

from app.config.settings import get_settings
from app.utils.logging import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="Polymarket Holder Edge MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Minimal HTTP health endpoint for local checks."""

    return {"status": "ok", "environment": settings.app_env}
