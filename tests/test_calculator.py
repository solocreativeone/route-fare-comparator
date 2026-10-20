import pandas as pd
import pytest

from calculator import compare_routes, monthly_cost, validate_fares


@pytest.fixture
def fares():
    return pd.DataFrame([
        {
            "origin": "Central Market", "destination": "University Gate",
            "mode": "Bus", "min_fare": 300, "max_fare": 500,
            "duration_min": 35, "source": "test", "date_collected": "2026-01-01",
        },
        {
            "origin": "Central Market", "destination": "University Gate",
            "mode": "Keke", "min_fare": 500, "max_fare": 800,
            "duration_min": 25, "source": "test", "date_collected": "2026-01-01",
        },
        {
            "origin": "Other", "destination": "Place",
            "mode": "Bus", "min_fare": 100, "max_fare": 200,
            "duration_min": 10, "source": "test", "date_collected": "2026-01-01",
        },
    ])


def test_compare_routes_returns_matching_records(fares):
    result = compare_routes(fares, "Central Market", "University Gate")
    assert len(result) == 2
    assert set(result["mode"]) == {"Bus", "Keke"}


def test_compare_routes_is_case_insensitive(fares):
    result = compare_routes(fares, "central market", "UNIVERSITY GATE")
    assert len(result) == 2


def test_monthly_cost_counts_one_way_trips():
    low, high = monthly_cost(300, 500, trips_per_week=10, weeks_per_month=4)
    assert low == 12000
    assert high == 20000


def test_validate_rejects_min_greater_than_max(fares):
    fares.loc[0, "min_fare"] = 700
    with pytest.raises(ValueError, match="min_fare"):
        validate_fares(fares)


def test_monthly_cost_rejects_negative_fare():
    with pytest.raises(ValueError):
        monthly_cost(-1, 100, 10)
