# Polymarket Holder Edge Bot

Research and decision-support MVP for identifying Polymarket markets where wallet quality looks asymmetric between `YES` and `NO`.

## MVP Status

Phase 1 is implemented:
- project skeleton and dependency management via `uv`
- typed config layer
- SQLAlchemy 2.x base setup
- initial ORM models
- Alembic migration setup
- CLI entrypoint
- minimal FastAPI health endpoint

Still missing for later phases:
- real Polymarket API clients
- ingestion jobs for markets, prices, and holders
- wallet scoring formulas
- side scoring and signal generation
- candidate ranking

## Stack

- Python 3.12+
- uv
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic Settings
- Typer
- structlog

## Project Structure

```text
app/
  api/           HTTP entrypoints
  clients/       Polymarket API wrappers
  config/        environment-driven settings
  db/            engine, session, metadata base
  domain/        pure formulas and scoring logic
  jobs/          ingestion and recompute jobs
  models/        SQLAlchemy ORM models
  repositories/  DB access helpers
  services/      orchestration layer
  utils/         shared logging and helpers
alembic/         migration configuration
tests/           smoke tests for the skeleton
```

## Quick Start

1. Install dependencies:

```bash
uv sync --extra dev
```

2. Create local env:

```bash
copy .env.example .env
```

3. Start PostgreSQL:

```bash
docker compose up -d postgres
```

4. Run migrations:

```bash
uv run pmhe db-upgrade
```

5. Check the app:

```bash
uv run pmhe show-settings
uv run pmhe health
uv run uvicorn app.api.main:app --reload
```

6. Open health endpoint:

```text
http://127.0.0.1:8000/health
```

## Configuration

Base configuration lives in `.env`. See `.env.example` for:
- database connection
- HTTP client settings
- placeholder scoring weights
- placeholder signal thresholds

All coefficients and thresholds are configured through settings rather than hardcoded in domain logic.

## Database Schema

Phase 1 creates these tables:
- `markets`
- `market_price_snapshots`
- `holder_snapshots`
- `wallet_market_stats`
- `wallet_aggregate_stats`
- `market_side_scores`
- `market_signals`

These tables are intentionally ready for later phases, even where population logic has not been implemented yet.

## CLI

Available commands in Phase 1:

```bash
uv run pmhe db-upgrade
uv run pmhe db-current
uv run pmhe health
uv run pmhe show-settings
```

The CLI is the primary MVP interface. Future ingestion and recompute commands will be added here.

## FastAPI

Phase 1 only exposes a thin HTTP layer:
- `GET /health`

API endpoints for markets, wallets, and signals will be added after the scoring pipeline exists.

## Assumptions and Limitations

- This is an MVP research system, not a trading bot.
- Polymarket external identifiers are stored as strings to avoid premature schema constraints.
- `smart_vwap`, side scores, and final signals are only schema placeholders in Phase 1.
- Actual Polymarket endpoint shapes are not locked yet; they will be isolated behind client modules in Phase 2.
- Missing metrics will use explicit fallbacks or TODOs instead of speculative abstractions.

## Phase Progress

### Phase 1

Implemented:
- project skeleton
- config layer
- DB foundation
- initial models
- Alembic setup
- README skeleton
- CLI and health API

Remaining before Phase 2:
- wire real Polymarket clients
- add ingestion jobs for active markets, price snapshots, and holder snapshots

Assumptions / blockers:
- local PostgreSQL must be reachable through `DATABASE_URL`
- Polymarket endpoint contracts still need validation during client implementation

## Next Step

Phase 2 will add public Polymarket clients and ingestion jobs for:
- active markets
- market price snapshots
- holder snapshots

That work will populate the schema created in Phase 1 without changing the core project structure.
