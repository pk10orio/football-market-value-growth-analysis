from pathlib import Path

import numpy as np
import pandas as pd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

try:
    import seaborn as sns
except ImportError:
    sns = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    valuations = pd.read_csv(RAW_DATA_DIR / "player_valuations.csv")
    players = pd.read_csv(RAW_DATA_DIR / "players.csv")
    return valuations, players


def prepare_valuations(valuations: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    players = players[["player_id", "name"]].copy()

    valuations["player_id"] = valuations["player_id"].astype(str).str.strip()
    players["player_id"] = players["player_id"].astype(str).str.strip()

    df = valuations.merge(players, on="player_id", how="left")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["market_value_in_eur"] = pd.to_numeric(df["market_value_in_eur"], errors="coerce")

    df = df.dropna(subset=["date", "market_value_in_eur"])
    df = df[(df["date"].dt.year >= 2013) & (df["date"].dt.year <= 2023)]
    df = df.sort_values(["player_id", "date"])
    return df


def calculate_club_periods(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["club_change"] = (
        df["current_club_id"] != df.groupby("player_id")["current_club_id"].shift(1)
    )
    df["club_period"] = df.groupby("player_id")["club_change"].cumsum()

    club_periods = (
        df.groupby(
            [
                "player_id",
                "name",
                "current_club_id",
                "current_club_name",
                "club_period",
            ]
        )
        .agg(
            start_date=("date", "first"),
            end_date=("date", "last"),
            initial_value=("market_value_in_eur", "first"),
            final_value=("market_value_in_eur", "last"),
        )
        .reset_index()
    )

    club_periods = club_periods[club_periods["initial_value"] > 0]
    club_periods["value_growth"] = (
        club_periods["final_value"] - club_periods["initial_value"]
    )
    club_periods["growth_pct"] = (
        club_periods["final_value"] / club_periods["initial_value"] - 1
    )
    club_periods["duration_days"] = (
        club_periods["end_date"] - club_periods["start_date"]
    ).dt.days

    return club_periods[
        (club_periods["duration_days"] > 90)
        & (club_periods["initial_value"] > 100_000)
    ]


def analyze_clubs(club_periods: pd.DataFrame) -> pd.DataFrame:
    club_analysis = (
        club_periods.groupby(["current_club_id", "current_club_name"])
        .agg(
            total_value_created=("value_growth", "sum"),
            avg_value_created=("value_growth", "mean"),
            median_value_created=("value_growth", "median"),
            avg_growth_pct=("growth_pct", "mean"),
            players=("player_id", "nunique"),
            positive_growth=("value_growth", lambda values: (values > 0).sum()),
            negative_growth=("value_growth", lambda values: (values < 0).sum()),
        )
        .reset_index()
    )

    club_analysis["value_per_player"] = (
        club_analysis["total_value_created"] / club_analysis["players"]
    )
    club_analysis["total_cases"] = (
        club_analysis["positive_growth"] + club_analysis["negative_growth"]
    )
    club_analysis["positive_rate"] = np.where(
        club_analysis["total_cases"] > 0,
        club_analysis["positive_growth"] / club_analysis["total_cases"],
        np.nan,
    )

    return club_analysis[club_analysis["players"] >= 5]


def save_outputs(club_analysis: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    top_clubs = club_analysis.sort_values(
        "total_value_created", ascending=False
    ).head(10)

    club_analysis.to_csv(TABLES_DIR / "club_value_analysis.csv", index=False)
    top_clubs.to_csv(TABLES_DIR / "top_10_clubs_value_created.csv", index=False)

    if plt is None:
        print("matplotlib is not installed. Tables were generated, but the chart was skipped.")
        return

    if sns is not None:
        plt.style.use("seaborn-v0_8")
        colors = sns.color_palette("Blues_r", len(top_clubs))
    else:
        colors = plt.cm.Blues_r(np.linspace(0.25, 0.9, len(top_clubs)))

    plt.figure(figsize=(12, 8))

    plt.barh(
        top_clubs["current_club_name"],
        top_clubs["total_value_created"] / 1e6,
        color=colors,
    )

    plt.title(
        "Top 10 Clubs - Total Value Created (EUR M)\n2013-2023",
        fontsize=16,
        fontweight="bold",
    )
    plt.xlabel("Total Value Created (EUR Millions)")
    plt.ylabel("Club")
    plt.gca().invert_yaxis()

    for index, value in enumerate(top_clubs["total_value_created"] / 1e6):
        plt.text(value * 1.01, index, f"EUR {value:.0f}M", va="center", fontsize=9)

    plt.margins(x=0.15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "club_value_analysis.png", dpi=150, bbox_inches="tight")


def main() -> None:
    valuations, players = load_data()
    prepared_valuations = prepare_valuations(valuations, players)
    club_periods = calculate_club_periods(prepared_valuations)
    club_analysis = analyze_clubs(club_periods)
    save_outputs(club_analysis)

    top_10 = club_analysis.nlargest(10, "total_value_created")
    print(top_10[["current_club_name", "total_value_created", "players", "positive_rate"]])


if __name__ == "__main__":
    main()
