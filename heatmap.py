import json
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from matplotlib.patches import Rectangle


def github_heatmap(submission_calendar):

    """
    submission_calendar:
        JSON string returned by LeetCode
    """

    # -------------------------
    # Parse submission calendar
    # -------------------------

    submission_dict = json.loads(submission_calendar)

    rows = []

    for timestamp, count in submission_dict.items():

        rows.append(
            {
                "date": datetime.fromtimestamp(int(timestamp)).date(),
                "count": count
            }
        )

    submissions = pd.DataFrame(rows)

    # -------------------------
    # Last 365 days
    # -------------------------

    end_date = datetime.today().date()

    start_date = end_date - timedelta(days=364)

    all_days = pd.DataFrame(
        {
            "date": pd.date_range(
                start_date,
                end_date,
                freq="D"
            ).date
        }
    )

    # Merge so days without submissions
    # also appear

    df = all_days.merge(
        submissions,
        on="date",
        how="left"
    )

    df["count"] = df["count"].fillna(0)

    # -------------------------
    # Calendar coordinates
    # -------------------------

    df["weekday"] = pd.to_datetime(
        df["date"]
    ).dt.weekday

    df["week"] = (
        (
            pd.to_datetime(df["date"])
            -
            pd.Timestamp(start_date)
        ).dt.days
        //
        7
    )

    df["month"] = pd.to_datetime(
        df["date"]
    ).dt.strftime("%b")

    # -------------------------
    # Create figure
    # -------------------------

    fig, ax = plt.subplots(
        figsize=(16,4)
    )

    ax.set_facecolor("#1a1a1a")

    fig.patch.set_facecolor("#1a1a1a")

    # LeetCode orange-yellow calendar colors
    colors = [
        "#2c2c2c",   # 0
        "#ffe6cc",   # 1-2
        "#ffb366",   # 3-5
        "#ff9333",   # 6-10
        "#ff7300"    # >10
    ]

    # -------------------------
    # Draw squares
    # -------------------------

    for _, row in df.iterrows():

        x = row["week"]

        y = 6 - row["weekday"]

        count = row["count"]

        if count == 0:
            color = colors[0]

        elif count <= 2:
            color = colors[1]

        elif count <= 5:
            color = colors[2]

        elif count <= 10:
            color = colors[3]

        else:
            color = colors[4]

        square = Rectangle(
            (x, y),
            0.82,
            0.82,
            facecolor=color,
            edgecolor="#1a1a1a",
            linewidth=1
        )

        ax.add_patch(square)
            # -------------------------
    # Month Labels
    # -------------------------

    month_positions = (
        df.groupby("month")["week"]
        .min()
        .reset_index()
    )

    for _, row in month_positions.iterrows():

        ax.text(
            row["week"],
            7.15,
            row["month"],
            color="#c9d1d9",
            fontsize=10,
            ha="left",
            va="bottom"
        )

    # -------------------------
    # Weekday Labels
    # -------------------------

    day_labels = [
        "Mon",
        "",
        "Wed",
        "",
        "Fri",
        "",
        "Sun"
    ]

    for i, label in enumerate(day_labels):

        if label != "":

            ax.text(
                -1.7,
                6 - i + 0.4,
                label,
                color="#8b949e",
                fontsize=9,
                ha="right",
                va="center"
            )

    # -------------------------
    # Legend
    # -------------------------

    legend_y = -1.35

    ax.text(
        df["week"].max() - 12,
        legend_y,
        "Less",
        color="#8b949e",
        fontsize=9,
        va="center"
    )

    legend_colors = colors

    start_x = df["week"].max() - 8

    for i, color in enumerate(legend_colors):

        square = Rectangle(
            (
                start_x + i * 1.1,
                legend_y - 0.25
            ),
            0.6,
            0.6,
            facecolor=color,
            edgecolor="#1a1a1a"
        )

        ax.add_patch(square)

    ax.text(
        start_x + len(legend_colors) * 1.1 + 0.4,
        legend_y,
        "More",
        color="#8b949e",
        fontsize=9,
        va="center"
    )

    # -------------------------
    # Title
    # -------------------------

    total_submissions = int(df["count"].sum())

    total_active_days = int((df["count"] > 0).sum())

    ax.text(
        0,
        8.2,
        f"{total_submissions} submissions in the last year",
        fontsize=15,
        color="white",
        fontweight="bold"
    )

    ax.text(
        df["week"].max() - 12,
        8.2,
        f"Active days: {total_active_days}",
        fontsize=10,
        color="#8b949e"
    )

    # -------------------------
    # Final Formatting
    # -------------------------

    ax.set_xlim(-2, df["week"].max() + 2)

    ax.set_ylim(-2, 9)

    ax.set_xticks([])

    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    return fig , df , colors