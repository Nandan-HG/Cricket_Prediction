
import numpy as np
import pandas as pd


def bootstrap_eye_in(
    faced_df,
    batter_name,
    n_bootstrap=1000,
    random_state=42
):
    rng = np.random.default_rng(random_state)

    player = faced_df[
        faced_df["batter"] == batter_name
    ].copy()

    if player.empty:
        raise ValueError(f"Batter not found: {batter_name}")

    # Separate the batter's first 10 balls and balls after 20.
    player["period"] = np.select(
        [
            player["ball_faced_number"] <= 10,
            player["ball_faced_number"] > 20
        ],
        ["first_10", "after_20"],
        default="middle"
    )

    # Calculate statistics separately for each innings.
    innings = (
        player[player["period"].isin(["first_10", "after_20"])]
        .groupby(["batter_innings_id", "period"])
        .agg(
            runs=("batter_runs", "sum"),
            balls=("batter_runs", "size")
        )
        .reset_index()
    )

    first = innings[innings["period"] == "first_10"]
    later = innings[innings["period"] == "after_20"]

    if len(first) < 10 or len(later) < 10:
        raise ValueError(
            "Insufficient innings for reliable bootstrap analysis."
        )

    # Observed scoring-rate difference.
    first_sr = first["runs"].sum() / first["balls"].sum() * 100
    later_sr = later["runs"].sum() / later["balls"].sum() * 100
    improvement = later_sr - first_sr

    # Resample complete innings, not individual deliveries.
    differences = []

    for _ in range(n_bootstrap):
        first_sample = first.iloc[
            rng.integers(0, len(first), size=len(first))
        ]

        later_sample = later.iloc[
            rng.integers(0, len(later), size=len(later))
        ]

        first_sample_sr = (
            first_sample["runs"].sum()
            / first_sample["balls"].sum() * 100
        )

        later_sample_sr = (
            later_sample["runs"].sum()
            / later_sample["balls"].sum() * 100
        )

        differences.append(later_sample_sr - first_sample_sr)
  
    return {
        "batter": batter_name,
        "first_period_innings": len(first),
        "later_period_innings": len(later),
        "first_10_strike_rate": first_sr,
        "after_20_strike_rate": later_sr,
        "improvement": improvement,
        "ci_lower": np.percentile(differences, 2.5),
        "ci_upper": np.percentile(differences, 97.5)
    }
