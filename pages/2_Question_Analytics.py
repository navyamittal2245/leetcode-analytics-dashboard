import streamlit as st
import pandas as pd

from charts import difficulty_chart, difficulty_pie_chart, topic_chart

# Get username from Home page
username = st.session_state.get("username")

if username is None:
    st.warning("👈 Please enter a username on the Home page first.")
    st.stop()

st.title("📊 Question Analytics")

progress = st.session_state.get("progress")

if progress is None:
    st.warning("Please enter a username on the Home page.")
    st.stop()

# Safety check
if (not progress or 
    "data" not in progress or 
    not progress["data"] or 
    progress["data"].get("userProfileUserQuestionProgressV2") is None):
    st.error("❌ Unable to fetch question progress analytics.")
    st.stop()

accepted = progress["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]

# Map difficulties to counts safely (handles dynamic list ordering, uppercase API, and missing keys)
difficulty_map = {"Easy": 0, "Medium": 0, "Hard": 0}
for item in accepted:
    diff = item.get("difficulty", "").title()
    count = item.get("count", 0)
    if diff in difficulty_map:
        difficulty_map[diff] = count

difficulties = ["Easy", "Medium", "Hard"]
counts = [difficulty_map["Easy"], difficulty_map["Medium"], difficulty_map["Hard"]]
total = sum(counts)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Solved", total)

with col2:
    st.metric("Easy 🟢", counts[0])

with col3:
    st.metric("Medium 🟡", counts[1])

with col4:
    st.metric("Hard 🔴", counts[2])

st.divider()

# Bar graph and pie chart    
bar_fig = difficulty_chart(difficulties, counts)
pie_fig = difficulty_pie_chart(difficulties, counts)

col_chart1, col_chart2 = st.columns([1, 1.2])

with col_chart1:
    st.pyplot(bar_fig)

with col_chart2:
    st.pyplot(pie_fig)

# topic wise analysis page
st.divider()
st.subheader("🏷️ Topic-wise Analysis")

skills = st.session_state.get("skills")

if (skills is None or 
    "data" not in skills or 
    not skills["data"] or 
    skills["data"].get("matchedUser") is None):
    st.warning("Topic-wise statistics not available for this user.")
else:
    tag_counts = skills["data"]["matchedUser"].get("tagProblemCounts")
    if not tag_counts:
        st.warning("No topic-wise data available.")
    else:
        all_topics = (
            tag_counts.get("fundamental", []) +
            tag_counts.get("intermediate", []) +
            tag_counts.get("advanced", [])
        )

        # Remove topics with 0 solved
        all_topics = [
            topic for topic in all_topics
            if topic.get("problemsSolved", 0) > 0
        ]

        if not all_topics:
            st.info("No topic-wise solve progress recorded.")
        else:
            # Sort descending
            all_topics.sort(
                key=lambda x: x.get("problemsSolved", 0),
                reverse=True
            )

            # Top 10 topics for charting
            top_topics = all_topics[:10]

            topic_names = [t["tagName"] for t in top_topics]
            solved = [t["problemsSolved"] for t in top_topics]

            fig = topic_chart(topic_names, solved)
            st.pyplot(fig)  

            # Show full topic progress table
            table_topics = [t["tagName"] for t in all_topics]
            table_solved = [t["problemsSolved"] for t in all_topics]

            topic_df = pd.DataFrame({
                "Topic": table_topics,
                "Problems Solved": table_solved
            })

            st.dataframe(
                topic_df,
                use_container_width=True,
                hide_index=True
            )

            # Strongest and weakest topics list      
            st.divider()
            col_strong, col_weak = st.columns(2)

            with col_strong:
                st.subheader("⭐ Strongest Topics")
                for topic in top_topics[:5]:
                    st.write(f"✅ **{topic['tagName']}** ({topic['problemsSolved']} solved)")

            with col_weak:
                st.subheader("⚠ Needs More Practice")
                # Sort ascending for weak topics
                weak_topics = sorted(
                    all_topics,
                    key=lambda x: x.get("problemsSolved", 0)
                )[:5]

                for topic in weak_topics:
                    st.write(f"📌 **{topic['tagName']}** ({topic['problemsSolved']} solved)")
