from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import PositionStatus


class WalletMarketStats(Base):
    __tablename__ = "wallet_market_stats"
    __table_args__ = (Index("ix_wallet_market_stats_wallet_updated_at", "wallet", "updated_at"),)

    wallet: Mapped[str] = mapped_column(String(128), primary_key=True)
    market_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    total_pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    realized_pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    unrealized_pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    tokens: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    position_status: Mapped[PositionStatus] = mapped_column(
        SqlEnum(PositionStatus, name="position_status"),
        nullable=False,
        default=PositionStatus.UNKNOWN,
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class WalletAggregateStats(Base):
    __tablename__ = "wallet_aggregate_stats"
    __table_args__ = (Index("ix_wallet_aggregate_stats_updated_at", "updated_at"),)

    wallet: Mapped[str] = mapped_column(String(128), primary_key=True)
    total_pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    total_volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    roi: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    resolved_markets_count: Mapped[int | None] = mapped_column(nullable=True)
    recent_90d_pnl: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    recent_90d_volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    recent_90d_roi: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    crypto_roi: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    fdv_roi: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    listing_roi: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    wallet_score: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True, index=True)
    score_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
