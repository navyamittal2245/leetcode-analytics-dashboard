import streamlit as st
import pandas as pd
from charts import contest_history_chart

contests = st.session_state.get("contests")

if contests is None:
    st.warning(" Please enter a username on the Home page first.")
    st.stop()

st.title("🏆 Contest Analytics")

# Safety check
if (not contests or 
    "data" not in contests or 
    not contests["data"] or 
    contests["data"].get("userContestRanking") is None):
    st.info("This user has not participated in any LeetCode contests yet.")
    st.stop()

contest_info = contests["data"]["userContestRanking"]
history = contests["data"].get("userContestRankingHistory", [])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rating ", f"{round(contest_info['rating']):,}")

with col2:
    st.metric("Global Rank ", f"{contest_info['globalRanking']:,}")

with col3:
    st.metric("Contests Attended ", f"{int(contest_info['attendedContestsCount'])}")

with col4:
    st.metric("Top Percentage ", f"{contest_info['topPercentage']:.2f}%")

st.divider()

# Filter for attended contests for clean plotting and reporting
attended_history = [c for c in history if c.get("attended", True)]

if not attended_history:
    st.info("No contest attendance history found.")
else:
    st.subheader("Contest Rating Progress")
    history_graph = contest_history_chart(history)
    st.pyplot(history_graph)

    st.subheader(" Contest Performance Table")

    contest_titles = []
    ratings = []
    rankings = []
    problems = []
    trend = []

    # Sort history descending (latest contests first) for the table
    for contest in sorted(attended_history, key=lambda x: x["contest"]["startTime"], reverse=True):
        contest_titles.append(contest["contest"]["title"])
        ratings.append(round(contest["rating"]))
        rankings.append(f"{contest['ranking']:,}")

        solved = f"{contest['problemsSolved']}/{contest['totalProblems']}"
        problems.append(solved)

        if contest["trendDirection"] == "UP":
            trend.append("📈 Up")
        elif contest["trendDirection"] == "DOWN":
            trend.append("📉 Down")
        else:
            trend.append("➖ Same")

    df = pd.DataFrame({
        "Contest": contest_titles,
        "Rating": ratings,
        "Rank": rankings,
        "Solved": problems,
        "Trend": trend
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )






