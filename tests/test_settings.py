from app.config.settings import Settings


def test_settings_load_from_env() -> None:
    settings = Settings(
        APP_ENV="test",
        DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/test_db",
    )

    assert settings.app_env == "test"
    assert settings.database_url.endswith("/test_db")
