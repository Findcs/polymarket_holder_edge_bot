from app.db.base import Base
from app.models import market, signal, wallet  # noqa: F401


def test_expected_tables_registered() -> None:
    expected = {
        "holder_snapshots",
        "market_price_snapshots",
        "market_side_scores",
        "market_signals",
        "markets",
        "wallet_aggregate_stats",
        "wallet_market_stats",
    }

    assert expected.issubset(Base.metadata.tables.keys())
