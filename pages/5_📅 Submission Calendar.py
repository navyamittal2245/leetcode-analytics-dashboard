import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime
from heatmap import github_heatmap

# ------------------ Load Calendar ------------------ #

calendar = st.session_state.get("calendar")
st.caption(
    "LeetCode contribution graph for the last 365 days."
)

if calendar is None:
    st.warning("👈 Please search a user on the Home page first.")
    st.stop()

# Safety boundary checks
if (not calendar or 
    "data" not in calendar or 
    not calendar["data"] or 
    calendar["data"].get("matchedUser") is None or
    calendar["data"]["matchedUser"].get("userCalendar") is None):
    st.warning("No submission calendar data available for this profile.")
    st.stop()

# ------------------ Header ------------------ #

st.title("📅 Submission Calendar")

calendar_info = calendar["data"]["matchedUser"]["userCalendar"]

fig, df , colors = github_heatmap(
    calendar_info["submissionCalendar"]
)
df["date"] = pd.to_datetime(df["date"])

df["Date"] = df["date"].dt.strftime("%d %b %Y")

df = df.sort_values(
    "date",
    ascending=False
).reset_index(drop=True)

st.pyplot(fig, use_container_width=True)


# ------------------ Legend ------------------ #

st.subheader("🟩 Legend")

legend_cols = st.columns(5)

labels = [
    "0",
    "1-2",
    "3-5",
    "6-10",
    "10+"
]

for col, color, label in zip(
    legend_cols,
    colors,
    labels
):

    with col:

        st.markdown(
            f"""
            <div style="
            width:25px;
            height:25px;
            background:{color};
            border:1px solid gray;
            margin-bottom:5px;">
            </div>

            {label}
            """,
            unsafe_allow_html=True
        )

st.divider()
# ------------------ Submission Statistics ------------------ #

st.subheader("📈 Submission Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Submission Days",
        int((df["count"] > 0).sum())
    )

with c2:
    st.metric(
        "Highest Daily Count",
        int(df["count"].max())
    )

with c3:
    st.metric(
        "Average / Day",
        f"{df['count'].mean():.1f}"
    )

with c4:
    st.metric(
        "Total Submissions",
        int(df["count"].sum())
    )

# ------------------ Busiest Weekday ------------------ #

weekday_counts = (
    df.groupby(
        df["date"].dt.day_name()
    )["count"].sum()
)

best_day = weekday_counts.idxmax()

st.info(
    f"🏅 Most productive weekday: **{best_day}**"
)

st.divider()

# ------------------ Submission Histogram ------------------ #

st.subheader("📊 Daily Submission Distribution")

fig2, ax = plt.subplots(figsize=(8,4))


ax.hist(
    df[df["count"] > 0]["count"],
    bins=10,
    color = "grey",
    edgecolor="black"
)

ax.set_title(
    "Submission Frequency"
)

ax.set_xlabel(
    "Submissions in a Day"
)

ax.set_ylabel(
    "Number of Days"
)

st.pyplot(fig2)

st.divider()

# ------------------ Top Active Days ------------------ #

st.subheader("🏆 Top 10 Most Active Days")


top_days = (
    df[df["count"] > 0]
    .sort_values(
        "count",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_days[
        ["Date", "count"]
    ].rename(
        columns={
            "count":"Submissions"
        }
    ),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ------------------ Search Submission History ------------------ #

st.subheader("📋 Submission History")

search = st.text_input(
    "🔍 Search by Date",
    placeholder="Example: Jun, 2026, 28 Jun"
)

filtered_df = (
    df[df["count"] > 0]
    .copy()
)

if search:

    filtered_df = filtered_df[
        filtered_df["Date"].str.contains(
            search,
            case=False
        )
    ]

show = st.selectbox(
    "Show latest",
    [10, 25, 50, 100, len(filtered_df)],
    index=2
)

history_table = (
    filtered_df
    .iloc[:show]
    [["Date", "count"]]
    .rename(
        columns={
            "count":"Submissions"
        }
    )
)

styled_table = (
    history_table.style
    .background_gradient(
        subset=["Submissions"],
        cmap="Greens"
    )
)

st.dataframe(
    styled_table,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ------------------ Download CSV ------------------ #

csv = filtered_df[
    ["Date", "count"]
].rename(
    columns={
        "count": "Submissions"
    }
).to_csv(index=False)

st.download_button(
    "⬇ Download Submission History",
    csv,
    file_name="submission_history.csv",
    mime="text/csv",
    use_container_width=True
)