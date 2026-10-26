
import pandas as pd
import pytest

from occupancy_utils import (
    prepare_hourly_data,
    split_hourly_data
)


def test_hourly_aggregation():
    """Check maximum headcount and reading count per hour."""
    times = pd.date_range(
        "2024-01-01 09:00",
        periods=3,
        freq="30min",
        tz="Australia/Melbourne"
    )

    data = pd.DataFrame({
        "floorspaceid": ["Room_A"] * 3,
        "local_time": times,
        "headcount": [2, 5, 3]
    })

    result = prepare_hourly_data(data)

    assert result["max_headcount"].tolist() == [5, 3]
    assert result["reading_count"].tolist() == [2, 1]


def test_missing_column():
    """Check that missing columns cause a ValueError."""
    data = pd.DataFrame({
        "floorspaceid": ["Room_A"],
        "headcount": [2]
    })

    with pytest.raises(ValueError):
        prepare_hourly_data(data)


def test_chronological_split():
    """Check non-overlapping chronological partitions."""
    data = pd.DataFrame({
        "local_time": pd.date_range(
            "2024-01-01",
            periods=30,
            freq="h",
            tz="Australia/Melbourne"
        ),
        "floorspaceid": ["Room_A"] * 30,
        "max_headcount": [1] * 30
    })

    dev, val, train, test = split_hourly_data(data)

    assert len(dev) + len(val) == len(train)
    assert len(train) + len(test) == len(data)
    assert dev["local_time"].max() < val["local_time"].min()
    assert val["local_time"].max() < test["local_time"].min()


def test_invalid_split_fraction():
    """Check that invalid split fractions are rejected."""
    data = pd.DataFrame({
        "local_time": pd.date_range(
            "2024-01-01",
            periods=30,
            freq="h",
            tz="Australia/Melbourne"
        )
    })

    with pytest.raises(ValueError):
        split_hourly_data(data, train_fraction=1.5)
