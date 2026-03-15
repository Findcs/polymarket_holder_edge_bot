from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Index, Numeric, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import TokenSide


class Market(Base):
    __tablename__ = "markets"

    market_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    subcategory: Mapped[str | None] = mapped_column(String(128), nullable=True)
    condition_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)
    yes_token_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    no_token_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MarketPriceSnapshot(Base):
    __tablename__ = "market_price_snapshots"
    __table_args__ = (Index("ix_market_price_snapshots_market_id_ts", "market_id", "ts"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    market_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    yes_bid: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    yes_ask: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    no_bid: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    no_ask: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    spread_yes: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    spread_no: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    volume_24h: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    liquidity: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)


class HolderSnapshot(Base):
    __tablename__ = "holder_snapshots"
    __table_args__ = (
        Index("ix_holder_snapshots_market_side_wallet_ts", "market_id", "token_side", "wallet", "snapshot_ts"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    market_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    token_side: Mapped[TokenSide] = mapped_column(SqlEnum(TokenSide, name="token_side"), nullable=False)
    wallet: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
