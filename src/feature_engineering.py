
import pandas as pd


def _is_true(value):
    """Convert common boolean representations to True or False."""
    if isinstance(value, bool):
        return value

    if pd.isna(value):
        return False

    return str(value).strip().lower() in {"true", "1", "yes"}


def _as_list(value):
    """Return a list, or an empty list if the value is missing."""
    return value if isinstance(value, list) else []


def batter_was_dismissed(row):
    """
    True only when the batter facing the delivery
    appears in the dismissed_players list.
    """
    dismissed_players = _as_list(row.get("dismissed_players"))
    batter = row.get("batter")

    return batter in dismissed_players


def prepare_batting_data(raw_df):
    """
    Prepare the batter-level ball-by-ball dataset.

    Expected raw columns:
    match_id, date, venue, innings, over, delivery_index,
    batter, bowler, batter_runs, total_runs, extras,
    is_wide, is_no_ball, dismissed_players, wicket_types.

    Wides are excluded from the returned faced-ball table.
    No-balls are retained as faced deliveries.
    """

    required_columns = [
        "match_id",
        "innings",
        "over",
        "delivery_index",
        "batter",
        "bowler",
        "batter_runs",
        "is_wide",
        "dismissed_players",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in raw_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Work on a copy so the raw dataset is not modified.
    df = raw_df.copy()

    # Normalize important columns.
    df["is_wide"] = df["is_wide"].apply(_is_true)

    if "is_no_ball" in df.columns:
        df["is_no_ball"] = df["is_no_ball"].apply(_is_true)
    else:
        df["is_no_ball"] = False

    df["batter_runs"] = pd.to_numeric(
        df["batter_runs"], errors="coerce"
    ).fillna(0)

    df["dismissed_players"] = (
        df["dismissed_players"].apply(_as_list)
    )

    # Sort deliveries in match order.
    df = df.sort_values(
        [
            "match_id",
            "innings",
            "over",
            "delivery_index",
        ]
    ).reset_index(drop=True)

    # Unique identifier for each batter's innings.
    df["batter_innings_id"] = (
        df["match_id"].astype(str)
        + "_"
        + df["innings"].astype(str)
        + "_"
        + df["batter"].astype(str)
    )

    # A wide does not count as a ball faced.
    # No-balls remain included in this project's ball count.
    df["counts_as_ball_faced"] = ~df["is_wide"]

    # Calculate the cumulative ball count before filtering wides.
    df["ball_faced_number"] = (
        df.groupby("batter_innings_id")[
            "counts_as_ball_faced"
        ]
        .cumsum()
        .astype(int)
    )

    # Identify dismissal of the batter who faced the delivery.
    df["dismissed"] = df.apply(
        batter_was_dismissed, axis=1
    )

    # Add match phase using zero-indexed overs.
    # Powerplay: overs 0-5; Middle: 6-14; Death: 15 onwards.
    if "over" in df.columns:
        df["phase"] = pd.cut(
            pd.to_numeric(df["over"], errors="coerce"),
            bins=[-1, 5, 14, float("inf")],
            labels=["Powerplay", "Middle", "Death"],
        )

    # Return only deliveries counted as balls faced.
    faced_df = df.loc[
        df["counts_as_ball_faced"]
        & (df["ball_faced_number"] > 0)
    ].copy()

    return faced_df.reset_index(drop=True)


def prepare_dismissal_events(raw_df):
    """
    Preserve dismissal events from all deliveries, including wides.

    Use this separate table when validating dismissal events.
    Do not count every dismissed player as the batter who faced
    the delivery.
    """

    df = raw_df.copy()

    df["is_wide"] = df["is_wide"].apply(_is_true)

    df["dismissed_players"] = (
        df["dismissed_players"].apply(_as_list)
    )

    df["batter_dismissed"] = df.apply(
        batter_was_dismissed, axis=1
    )

    # Keep deliveries that actually contain dismissal events.
    df["has_dismissal"] = (
        df["dismissed_players"].str.len() > 0
    )

    return df.loc[df["has_dismissal"]].reset_index(drop=True)
