from typer.testing import CliRunner

from app.cli import app


runner = CliRunner()


def test_show_settings_hides_database_url() -> None:
    result = runner.invoke(app, ["show-settings"])

    assert result.exit_code == 0
    assert "database_url=<hidden>" in result.stdout
