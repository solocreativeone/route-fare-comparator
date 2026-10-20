"""Pure fare calculation functions used by the app and tests."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {
    "origin", "destination", "mode", "min_fare", "max_fare",
    "duration_min", "source", "date_collected"
}


def validate_fares(fares: pd.DataFrame) -> None:
    """Raise ValueError when fare data is missing required fields or is invalid."""
    missing = REQUIRED_COLUMNS - set(fares.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    numeric_columns = ["min_fare", "max_fare", "duration_min"]
    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(fares[column]):
            raise ValueError(f"{column} must contain numeric values")

    if (fares[["min_fare", "max_fare", "duration_min"]] < 0).any().any():
        raise ValueError("Fare and duration values cannot be negative")

    if (fares["min_fare"] > fares["max_fare"]).any():
        raise ValueError("min_fare cannot be greater than max_fare")


def compare_routes(
    fares: pd.DataFrame, origin: str, destination: str
) -> pd.DataFrame:
    """Return fare records matching an origin/destination pair."""
    validate_fares(fares)
    mask = (
        fares["origin"].astype(str).str.strip().str.casefold().eq(origin.strip().casefold())
        & fares["destination"].astype(str).str.strip().str.casefold().eq(destination.strip().casefold())
    )
    return fares.loc[mask].copy()


def monthly_cost(
    min_fare: float,
    max_fare: float,
    trips_per_week: int,
    weeks_per_month: float = 4.33,
) -> tuple[float, float]:
    """Calculate low/high monthly costs from one-way fares and trip frequency.

    trips_per_week counts one-way journeys. For a daily return commute on five
    days, pass 10 trips per week.
    """
    if min_fare < 0 or max_fare < 0:
        raise ValueError("Fares cannot be negative")
    if min_fare > max_fare:
        raise ValueError("min_fare cannot be greater than max_fare")
    if trips_per_week < 0:
        raise ValueError("trips_per_week cannot be negative")
    if weeks_per_month < 0:
        raise ValueError("weeks_per_month cannot be negative")

    multiplier = trips_per_week * weeks_per_month
    return min_fare * multiplier, max_fare * multiplier
