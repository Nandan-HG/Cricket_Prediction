
import json
from pathlib import Path
import pandas as pd


def load_ipl_data(raw_dir):
    rows = []

    for file_path in Path(raw_dir).glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            match = json.load(file)

        info = match.get("info", {})
        match_id = file_path.stem
        dates = info.get("dates", [])

        for innings_no, innings in enumerate(
            match.get("innings", []), start=1
        ):
            for over_data in innings.get("overs", []):
                over_number = over_data.get("over", 0)

                for delivery_index, delivery in enumerate(
                    over_data.get("deliveries", []), start=1
                ):
                    extras = delivery.get("extras", {})
                    wickets = delivery.get("wickets", [])

                    rows.append({
                        "match_id": match_id,
                        "date": dates[0] if dates else None,
                        "venue": info.get("venue", "Unknown"),
                        "innings": innings_no,
                        "over": over_number,
                        "delivery_index": delivery_index,
                        "batter": delivery.get("batter"),
                        "bowler": delivery.get("bowler"),
                        "batter_runs": delivery.get(
                            "runs", {}
                        ).get("batter", 0),
                        "total_runs": delivery.get(
                            "runs", {}
                        ).get("total", 0),
                        "extras": extras,
                        "is_wide": "wides" in extras,
                        "is_no_ball": "noballs" in extras,
                        "dismissed_players": [
                            w.get("player_out") for w in wickets
                        ],
                        "wicket_types": [
                            w.get("kind") for w in wickets
                        ],
                    })

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError(
            "No deliveries loaded. Check the JSON folder."
        )

    return df
