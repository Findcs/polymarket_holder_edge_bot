"""Initial MVP schema."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260313_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


token_side = sa.Enum("YES", "NO", name="token_side")
smart_side = sa.Enum("YES", "NO", "NONE", name="smart_side")
position_status = sa.Enum("OPEN", "CLOSED", "RESOLVED", "UNKNOWN", name="position_status")


def upgrade() -> None:
    token_side.create(op.get_bind(), checkfirst=True)
    smart_side.create(op.get_bind(), checkfirst=True)
    position_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "markets",
        sa.Column("market_id", sa.String(length=128), primary_key=True),
        sa.Column("event_id", sa.String(length=128), nullable=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=True),
        sa.Column("subcategory", sa.String(length=128), nullable=True),
        sa.Column("condition_id", sa.String(length=128), nullable=True),
        sa.Column("yes_token_id", sa.String(length=128), nullable=True),
        sa.Column("no_token_id", sa.String(length=128), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("closed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("condition_id", name="uq_markets_condition_id"),
    )
    op.create_index("ix_markets_event_id", "markets", ["event_id"], unique=False)
    op.create_index("ix_markets_category", "markets", ["category"], unique=False)

    op.create_table(
        "market_price_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("market_id", sa.String(length=128), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("yes_bid", sa.Numeric(20, 8), nullable=True),
        sa.Column("yes_ask", sa.Numeric(20, 8), nullable=True),
        sa.Column("no_bid", sa.Numeric(20, 8), nullable=True),
        sa.Column("no_ask", sa.Numeric(20, 8), nullable=True),
        sa.Column("spread_yes", sa.Numeric(20, 8), nullable=True),
        sa.Column("spread_no", sa.Numeric(20, 8), nullable=True),
        sa.Column("volume_24h", sa.Numeric(20, 8), nullable=True),
        sa.Column("liquidity", sa.Numeric(20, 8), nullable=True),
    )
    op.create_index("ix_market_price_snapshots_market_id", "market_price_snapshots", ["market_id"], unique=False)
    op.create_index("ix_market_price_snapshots_ts", "market_price_snapshots", ["ts"], unique=False)
    op.create_index(
        "ix_market_price_snapshots_market_id_ts",
        "market_price_snapshots",
        ["market_id", "ts"],
        unique=False,
    )

    op.create_table(
        "holder_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("market_id", sa.String(length=128), nullable=False),
        sa.Column("token_side", token_side, nullable=False),
        sa.Column("wallet", sa.String(length=128), nullable=False),
        sa.Column("amount", sa.Numeric(20, 8), nullable=False),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_holder_snapshots_market_id", "holder_snapshots", ["market_id"], unique=False)
    op.create_index("ix_holder_snapshots_wallet", "holder_snapshots", ["wallet"], unique=False)
    op.create_index("ix_holder_snapshots_snapshot_ts", "holder_snapshots", ["snapshot_ts"], unique=False)
    op.create_index(
        "ix_holder_snapshots_market_side_wallet_ts",
        "holder_snapshots",
        ["market_id", "token_side", "wallet", "snapshot_ts"],
        unique=False,
    )

    op.create_table(
        "wallet_market_stats",
        sa.Column("wallet", sa.String(length=128), primary_key=True),
        sa.Column("market_id", sa.String(length=128), primary_key=True),
        sa.Column("category", sa.String(length=128), nullable=True),
        sa.Column("total_pnl", sa.Numeric(20, 8), nullable=True),
        sa.Column("realized_pnl", sa.Numeric(20, 8), nullable=True),
        sa.Column("unrealized_pnl", sa.Numeric(20, 8), nullable=True),
        sa.Column("volume", sa.Numeric(20, 8), nullable=True),
        sa.Column("tokens", sa.Numeric(20, 8), nullable=True),
        sa.Column("position_status", position_status, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_wallet_market_stats_category", "wallet_market_stats", ["category"], unique=False)
    op.create_index(
        "ix_wallet_market_stats_wallet_updated_at",
        "wallet_market_stats",
        ["wallet", "updated_at"],
        unique=False,
    )

    op.create_table(
        "wallet_aggregate_stats",
        sa.Column("wallet", sa.String(length=128), primary_key=True),
        sa.Column("total_pnl", sa.Numeric(20, 8), nullable=True),
        sa.Column("total_volume", sa.Numeric(20, 8), nullable=True),
        sa.Column("roi", sa.Numeric(20, 8), nullable=True),
        sa.Column("resolved_markets_count", sa.Integer(), nullable=True),
        sa.Column("recent_90d_pnl", sa.Numeric(20, 8), nullable=True),
        sa.Column("recent_90d_volume", sa.Numeric(20, 8), nullable=True),
        sa.Column("recent_90d_roi", sa.Numeric(20, 8), nullable=True),
        sa.Column("crypto_roi", sa.Numeric(20, 8), nullable=True),
        sa.Column("fdv_roi", sa.Numeric(20, 8), nullable=True),
        sa.Column("listing_roi", sa.Numeric(20, 8), nullable=True),
        sa.Column("wallet_score", sa.Numeric(20, 8), nullable=True),
        sa.Column("score_version", sa.String(length=64), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_wallet_aggregate_stats_wallet_score", "wallet_aggregate_stats", ["wallet_score"], unique=False)
    op.create_index("ix_wallet_aggregate_stats_updated_at", "wallet_aggregate_stats", ["updated_at"], unique=False)

    op.create_table(
        "market_side_scores",
        sa.Column("market_id", sa.String(length=128), primary_key=True),
        sa.Column("side", token_side, primary_key=True),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), primary_key=True),
        sa.Column("side_score", sa.Numeric(20, 8), nullable=True),
        sa.Column("side_score_avg", sa.Numeric(20, 8), nullable=True),
        sa.Column("elite_mass", sa.Numeric(20, 8), nullable=True),
        sa.Column("holder_count", sa.Integer(), nullable=True),
        sa.Column("estimated_smart_vwap", sa.Numeric(20, 8), nullable=True),
        sa.Column("current_entry_price", sa.Numeric(20, 8), nullable=True),
        sa.Column("entry_edge", sa.Numeric(20, 8), nullable=True),
    )
    op.create_index(
        "ix_market_side_scores_market_id_snapshot_ts",
        "market_side_scores",
        ["market_id", "snapshot_ts"],
        unique=False,
    )

    op.create_table(
        "market_signals",
        sa.Column("market_id", sa.String(length=128), primary_key=True),
        sa.Column("snapshot_ts", sa.DateTime(timezone=True), primary_key=True),
        sa.Column("smart_side", smart_side, nullable=False),
        sa.Column("quality_gap", sa.Numeric(20, 8), nullable=True),
        sa.Column("relative_gap", sa.Numeric(20, 8), nullable=True),
        sa.Column("entry_edge", sa.Numeric(20, 8), nullable=True),
        sa.Column("confidence", sa.Numeric(20, 8), nullable=True),
        sa.Column("final_signal", sa.String(length=64), nullable=True),
        sa.Column("explanation_json", sa.JSON(), nullable=True),
    )
    op.create_index(
        "ix_market_signals_snapshot_ts_final_signal",
        "market_signals",
        ["snapshot_ts", "final_signal"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_market_signals_snapshot_ts_final_signal", table_name="market_signals")
    op.drop_table("market_signals")

    op.drop_index("ix_market_side_scores_market_id_snapshot_ts", table_name="market_side_scores")
    op.drop_table("market_side_scores")

    op.drop_index("ix_wallet_aggregate_stats_updated_at", table_name="wallet_aggregate_stats")
    op.drop_index("ix_wallet_aggregate_stats_wallet_score", table_name="wallet_aggregate_stats")
    op.drop_table("wallet_aggregate_stats")

    op.drop_index("ix_wallet_market_stats_wallet_updated_at", table_name="wallet_market_stats")
    op.drop_index("ix_wallet_market_stats_category", table_name="wallet_market_stats")
    op.drop_table("wallet_market_stats")

    op.drop_index("ix_holder_snapshots_market_side_wallet_ts", table_name="holder_snapshots")
    op.drop_index("ix_holder_snapshots_snapshot_ts", table_name="holder_snapshots")
    op.drop_index("ix_holder_snapshots_wallet", table_name="holder_snapshots")
    op.drop_index("ix_holder_snapshots_market_id", table_name="holder_snapshots")
    op.drop_table("holder_snapshots")

    op.drop_index("ix_market_price_snapshots_market_id_ts", table_name="market_price_snapshots")
    op.drop_index("ix_market_price_snapshots_ts", table_name="market_price_snapshots")
    op.drop_index("ix_market_price_snapshots_market_id", table_name="market_price_snapshots")
    op.drop_table("market_price_snapshots")

    op.drop_index("ix_markets_category", table_name="markets")
    op.drop_index("ix_markets_event_id", table_name="markets")
    op.drop_table("markets")

    position_status.drop(op.get_bind(), checkfirst=True)
    smart_side.drop(op.get_bind(), checkfirst=True)
    token_side.drop(op.get_bind(), checkfirst=True)
