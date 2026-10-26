
import pandas as pd


def prepare_hourly_data(data):
    """Aggregate recorded headcounts by monitored space and hour."""
    required = ["floorspaceid", "local_time", "headcount"]
    missing = [c for c in required if c not in data.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    hourly = (
        data.groupby([
            "floorspaceid",
            pd.Grouper(key="local_time", freq="h")
        ])
        .agg(
            max_headcount=("headcount", "max"),
            reading_count=("headcount", "size")
        )
        .reset_index()
    )

    hourly["hour"] = hourly["local_time"].dt.hour
    hourly["day_of_week"] = hourly["local_time"].dt.dayofweek

    return hourly.sort_values(
        ["local_time", "floorspaceid"]
    ).reset_index(drop=True)


def split_hourly_data(data, train_fraction=0.8, dev_fraction=0.8):
    """Split hourly observations into chronological data partitions."""
    if not 0 < train_fraction < 1 or not 0 < dev_fraction < 1:
        raise ValueError("Split fractions must be between 0 and 1")

    data = data.sort_values("local_time").reset_index(drop=True)
    times = data["local_time"].drop_duplicates().sort_values()

    test_start = times.iloc[int(len(times) * train_fraction)]
    train = data[data["local_time"] < test_start].copy()
    test = data[data["local_time"] >= test_start].copy()

    train_times = train["local_time"].drop_duplicates().sort_values()
    val_start = train_times.iloc[int(len(train_times) * dev_fraction)]

    dev = train[train["local_time"] < val_start].copy()
    val = train[train["local_time"] >= val_start].copy()

    return dev, val, train, test
