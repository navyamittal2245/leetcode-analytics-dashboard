import matplotlib.pyplot as plt

def difficulty_chart(difficulties, counts):
    fig_1, ax = plt.subplots(figsize=(3.5, 4.5))
    
    # Theme configuration (transparent background for theme adaptability)
    fig_1.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Safeguard for 0 solved questions
    if sum(counts) == 0:
        ax.text(0.5, 0.5, "No problems solved yet", ha="center", va="center", color="#8b949e", fontsize=11)
        ax.set_title("Problems by Difficulty", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
        ax.axis("off")
        fig_1.tight_layout()
        return fig_1
    
    # LeetCode specific brand colors: Easy (Teal), Medium (Yellow), Hard (Red)
    bars = ax.bar(
        difficulties,
        counts,
        color=["#00b8a3", "#ffc01e", "#ef4743"],
        width=0.6,
        edgecolor='none'
    )

    ax.set_title("Problems by Difficulty", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
    ax.set_ylabel("Problems Solved", fontsize=9, color="#8b949e")
    
    # Style ticks and axes
    ax.tick_params(colors="#8b949e", labelsize=9)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#8b949e")
        ax.spines[spine].set_alpha(0.3)

    # Add count values above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + max(counts)*0.01,
            str(height),
            ha="center",
            va="bottom",
            color="#8b949e",
            fontsize=9,
            fontweight="bold"
        )

    fig_1.tight_layout()
    return fig_1

def difficulty_pie_chart(difficulties, counts):
    fig_2, ax = plt.subplots(figsize=(6, 5))
    fig_2.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Safeguard for 0 solved questions
    if sum(counts) == 0:
        ax.text(0.8, 0.8, "No problems solved yet", ha="center", va="center", color="#8b949e", fontsize=11)
        ax.set_title("Difficulty Distribution", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
        ax.axis("off")
        fig_2.tight_layout()
        return fig_2
    
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=difficulties,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#00b8a3", "#ffc01e", "#ef4743"],
        wedgeprops={"width": 0.6, "edgecolor": "none"},
        textprops={"color": "#8b949e", "fontsize": 10}
    )
    
    # Make percentages bold and white for contrast
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(9)
        
    ax.set_title("Difficulty Distribution", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
    
    fig_2.tight_layout()
    return fig_2

def contest_history_chart(history):
    ratings = []
    contest_names = []

    for contest in history:
        # Filter for attended contests only to avoid flatlines from unattended ones
        if contest.get("attended", True):
            ratings.append(contest["rating"])
            title = contest["contest"]["title"]
            # Abbreviate contest names
            title = title.replace("Weekly Contest ", "WC ").replace("Biweekly Contest ", "BC ")
            contest_names.append(title)

    fig_3, ax = plt.subplots(figsize=(9, 4.5))
    fig_3.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Plot with clean, modern line and dots matching LeetCode yellow theme
    ax.plot(
        contest_names,
        ratings,
        marker="o",
        markersize=5,
        linewidth=2,
        color="#ffa116",        # LeetCode Yellow
        markerfacecolor="#282828", # Dark Grey center
        markeredgecolor="#ffa116", # Yellow border
        markeredgewidth=1.5
    )

    ax.set_title("Contest Rating Progress", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
    ax.set_xlabel("Contests Attended", fontsize=9, color="#8b949e")
    ax.set_ylabel("Rating", fontsize=9, color="#8b949e")

    ax.grid(color="#8b949e", alpha=0.1, linestyle="--")
    
    # Style ticks and axes
    ax.tick_params(colors="#8b949e", labelsize=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#8b949e")
        ax.spines[spine].set_alpha(0.3)
        
    ax.tick_params(axis="x", rotation=45)
    
    # Prevent x-axis label clutter if there are many contests
    if len(contest_names) > 15:
        every_n = len(contest_names) // 10
        indices = list(range(0, len(contest_names), every_n))
        ax.set_xticks(indices)
        ax.set_xticklabels([contest_names[i] for i in indices])

    fig_3.tight_layout()
    return fig_3

def topic_chart(topic_names, solved):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Soft, modern LeetCode Yellow color
    bars = ax.barh(topic_names, solved, color="#ffa116", alpha=0.85, height=0.6)

    ax.set_title("Topic-wise Problems Solved", fontsize=11, color="#8b949e", fontweight="bold", pad=15)
    ax.set_xlabel("Problems Solved", fontsize=9, color="#8b949e")
    
    # Style ticks and axes
    ax.tick_params(colors="#8b949e", labelsize=9)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#8b949e")
        ax.spines[spine].set_alpha(0.3)

    ax.invert_yaxis()

    # Add numeric labels to the right of horizontal bars
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + max(solved)*0.01 + 0.1,
            bar.get_y() + bar.get_height()/2,
            str(int(width)),
            va="center",
            ha="left",
            color="#8b949e",
            fontsize=9,
            fontweight="bold"
        )

    fig.tight_layout()
    return fig


    
