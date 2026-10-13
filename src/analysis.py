
import pandas as pd


def calculate_ball_metrics(faced_df, min_innings=50):
    """
    Calculate scoring rate and dismissal frequency at each
    ball-faced position.

    Only deliveries counted as balls faced are included.
    Wide-ball dismissals are not assigned to a faced-ball
    position; they should be reported separately.
    """

    required = [
        "ball_faced_number",
        "batter_innings_id",
        "batter_runs",
        "dismissed",
    ]

    missing = [col for col in required if col not in faced_df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = faced_df.copy()

    metrics = (
        df.groupby("ball_faced_number")
        .agg(
            batter_innings=("batter_innings_id", "nunique"),
            dismissals=("dismissed", "sum"),
            total_runs=("batter_runs", "sum"),
            balls=("batter_runs", "size"),
        )
        .reset_index()
        .sort_values("ball_faced_number")
    )

    metrics["dismissal_rate_pct"] = (
        metrics["dismissals"]
        / metrics["batter_innings"]
        * 100
    )

    metrics["strike_rate"] = (
        metrics["total_runs"]
        / metrics["balls"]
        * 100
    )

    metrics["strike_rate_smooth"] = (
        metrics["strike_rate"]
        .rolling(window=5, min_periods=1)
        .mean()
    )

    metrics["enough_data"] = (
        metrics["batter_innings"] >= min_innings
    )

    return metrics.reset_index(drop=True)


def calculate_phase_metrics(faced_df, min_innings=50):
    """
    Calculate ball-position scoring and dismissal metrics
    separately for Powerplay, Middle, and Death phases.

    Phase is determined by the over in which the delivery
    occurred, not by the batter's innings age.
    """

    required = [
        "phase",
        "ball_faced_number",
        "batter_innings_id",
        "batter_runs",
        "dismissed",
    ]

    missing = [col for col in required if col not in faced_df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = faced_df.copy()

    metrics = (
        df.dropna(subset=["phase"])
        .groupby(
            ["phase", "ball_faced_number"],
            observed=True,
        )
        .agg(
            batter_innings=("batter_innings_id", "nunique"),
            dismissals=("dismissed", "sum"),
            total_runs=("batter_runs", "sum"),
            balls=("batter_runs", "size"),
        )
        .reset_index()
        .sort_values(["phase", "ball_faced_number"])
    )

    metrics["dismissal_rate_pct"] = (
        metrics["dismissals"]
        / metrics["batter_innings"]
        * 100
    )

    metrics["strike_rate"] = (
        metrics["total_runs"]
        / metrics["balls"]
        * 100
    )

    metrics["enough_data"] = (
        metrics["batter_innings"] >= min_innings
    )

    return metrics.reset_index(drop=True)


def summarize_wide_dismissals(raw_df):
    """
    Summarize dismissals occurring on wides separately.
    These events are not balls faced.
    """

    required = ["is_wide", "dismissed_players", "wicket_types"]

    missing = [col for col in required if col not in raw_df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = raw_df.copy()

    df["is_wide"] = df["is_wide"].map(
        lambda x: (
            x if isinstance(x, bool)
            else str(x).strip().lower() in {"true", "1", "yes"}
        )
    )

    df["dismissed_players"] = df["dismissed_players"].map(
        lambda x: x if isinstance(x, list) else []
    )

    wide_dismissals = df[
        df["is_wide"]
        & df["dismissed_players"].map(len).gt(0)
    ].copy()

    return wide_dismissals
