
import pandas as pd


def calculate_eye_in_index(faced_df, min_balls=100):
    df = faced_df.copy()

    # Group each batter's deliveries by their ball position.
    df["period"] = pd.cut(
        df["ball_faced_number"],
        bins=[0, 10, 20, float("inf")],
        labels=["First 10", "Balls 11-20", "After 20"]
    )

    summary = (
        df[df["period"].isin(["First 10", "After 20"])]
        .groupby(["batter", "period"], observed=True)
        .agg(
            balls=("batter_runs", "size"),
            runs=("batter_runs", "sum"),
            dismissals=("dismissed", "sum")
        )
        .reset_index()
    )

    summary["strike_rate"] = (
        summary["runs"] / summary["balls"] * 100
    )

    summary["dismissal_rate_pct"] = (
        summary["dismissals"] / summary["balls"] * 100
    )

    strike_rates = summary.pivot(
        index="batter",
        columns="period",
        values="strike_rate"
    )

    dismissal_rates = summary.pivot(
        index="batter",
        columns="period",
        values="dismissal_rate_pct"
    )

    counts = summary.pivot(
        index="batter",
        columns="period",
        values="balls"
    )

    result = pd.DataFrame(index=strike_rates.index)

    result["first_10_sr"] = strike_rates.get("First 10")
    result["after_20_sr"] = strike_rates.get("After 20")

    result["first_10_dismissal_pct"] = (
        dismissal_rates.get("First 10")
    )
    result["after_20_dismissal_pct"] = (
        dismissal_rates.get("After 20")
    )

    result["scoring_improvement"] = (
        result["after_20_sr"] - result["first_10_sr"]
    )

    result["dismissal_rate_change_pp"] = (
        result["after_20_dismissal_pct"]
        - result["first_10_dismissal_pct"]
    )

    result["first_10_balls"] = counts.get("First 10")
    result["after_20_balls"] = counts.get("After 20")

    result = result[
        (result["first_10_balls"] >= min_balls)
        & (result["after_20_balls"] >= min_balls)
    ].copy()

    return result.sort_values(
        "scoring_improvement", ascending=False
    ).reset_index()
