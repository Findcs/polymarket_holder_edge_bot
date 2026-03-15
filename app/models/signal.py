from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import SmartSide, TokenSide


class MarketSideScore(Base):
    __tablename__ = "market_side_scores"
    __table_args__ = (Index("ix_market_side_scores_market_id_snapshot_ts", "market_id", "snapshot_ts"),)

    market_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    side: Mapped[TokenSide] = mapped_column(SqlEnum(TokenSide, name="token_side"), primary_key=True)
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    side_score: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    side_score_avg: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    elite_mass: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    holder_count: Mapped[int | None] = mapped_column(nullable=True)
    estimated_smart_vwap: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    current_entry_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    entry_edge: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)


class MarketSignal(Base):
    __tablename__ = "market_signals"
    __table_args__ = (Index("ix_market_signals_snapshot_ts_final_signal", "snapshot_ts", "final_signal"),)

    market_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    snapshot_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    smart_side: Mapped[SmartSide] = mapped_column(SqlEnum(SmartSide, name="smart_side"), nullable=False)
    quality_gap: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    relative_gap: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    entry_edge: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    final_signal: Mapped[str | None] = mapped_column(String(64), nullable=True)
    explanation_json: Mapped[dict[str, str] | None] = mapped_column(nullable=True)
