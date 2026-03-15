from typing import Any

import typer
from alembic import command
from alembic.config import Config

from app.api.main import app as fastapi_app
from app.config.settings import get_settings
from app.db.session import check_database_connection
from app.utils.logging import configure_logging


app = typer.Typer(help="Polymarket holder edge MVP CLI.")


def get_alembic_config() -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", get_settings().database_url)
    return config


@app.callback()
def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command("db-upgrade")
def db_upgrade(revision: str = "head") -> None:
    """Apply Alembic migrations up to the requested revision."""

    command.upgrade(get_alembic_config(), revision)
    typer.echo(f"Database upgraded to {revision}.")


@app.command("db-current")
def db_current() -> None:
    """Print the current Alembic revision."""

    command.current(get_alembic_config())


@app.command("health")
def health() -> None:
    """Run a minimal process and database health check."""

    try:
        db_ok = check_database_connection()
        typer.echo(f"status=ok database={db_ok} api_title={fastapi_app.title}")
    except Exception as exc:  # pragma: no cover - defensive CLI surface
        typer.echo(f"status=error detail={exc}", err=True)
        raise typer.Exit(code=1) from exc


@app.command("show-settings")
def show_settings() -> None:
    """Print sanitized runtime settings."""

    settings = get_settings()
    payload: dict[str, Any] = settings.model_dump()
    payload["database_url"] = "<hidden>"
    for key, value in payload.items():
        typer.echo(f"{key}={value}")


if __name__ == "__main__":
    app()
