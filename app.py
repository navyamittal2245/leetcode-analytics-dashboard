import streamlit as st
import json
import os
from fetch_data import (
    get_user_profile,
    get_user_progress,
    get_user_contests, 
    get_user_skills,
    get_user_calendar
)

st.set_page_config(
    page_title="LeetCode Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------- HERO --------------------

st.title(" LeetCode Analytics Dashboard")

st.caption(
    "Analyze any public LeetCode profile with detailed analytics, interactive visualizations, AI-powered insights, and downloadable reports."
)

st.divider()

# -------------------- SEARCH --------------------
# Recent searches (stored only for the current user's session)
if "recent_searches" not in st.session_state:
    st.session_state["recent_searches"] = []

usernames = st.session_state["recent_searches"]

st.subheader(" Search Profile")

if "username" in st.session_state:
    st.success(f"Current Profile: {st.session_state['username']}")

    if st.button("🔄 Search Another User", use_container_width=True):
        for key in ["username", "profile", "progress", "contests", "skills", "calendar"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

else:
    # Double input system: text input for typing new user, selectbox for picking recent searches
    col_input, col_recent = st.columns([2, 1])
    with col_input:
        username_input = st.text_input(
            "Enter LeetCode Username",
            placeholder="Type a username..."
        )
    with col_recent:
        recent_selected = st.selectbox(
            "Recent Searches",
            options=[""] + usernames,
            format_func=lambda x: "Select recent..." if x == "" else x
        )
    
    # Determine the username to search
    username = username_input.strip() if username_input.strip() else recent_selected

    if st.button("🚀 Analyze Profile", use_container_width=True):
        if not username:
            st.warning("Please enter a username or select a recent one.")
            st.stop()

        with st.spinner("Fetching LeetCode data..."):
            try:
                # 1. Fetch profile first to verify user exists
                profile = get_user_profile(username)
                
                if (not profile or 
                    "data" not in profile or 
                    not profile["data"] or 
                    profile["data"].get("matchedUser") is None):
                    st.error(" LeetCode user not found. Please verify the username.")
                    st.stop()

                # 2. Fetch the rest of the details
                progress = get_user_progress(username)
                contests = get_user_contests(username)
                skills = get_user_skills(username)
                calendar = get_user_calendar(username)

                # Save everything to session state
                st.session_state["username"] = username
                st.session_state["profile"] = profile
                st.session_state["progress"] = progress
                st.session_state["contests"] = contests
                st.session_state["skills"] = skills
                st.session_state["calendar"] = calendar

                # Save username to recent searches
                if username in usernames:
                    usernames.remove(username)

                usernames.insert(0, username)

                # Keep only the 10 most recent searches
                st.session_state["recent_searches"] = usernames[:10]

                st.success(" Profile loaded successfully!")
                st.info(" Open pages from the sidebar to explore analytics.")
                st.rerun()

            except Exception as e:
                st.error(f" Failed to fetch LeetCode data: {str(e)}")


st.divider()

# Helper for rendering LeetCode styled feature cards
def feature_card(title,  items):
    items_html = "".join([f"<li style='margin-bottom:6px;'>{item}</li>" for item in items])
    card_html = f"""
    <div style="
        background-color: #282828;
        border-radius: 8px;
        padding: 20px;
        border-left: 5px solid #ffa116;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        min-height: 250px;
    ">
        <h4 style="color: #ffa116; margin-top:0; font-size:1.15rem; font-weight:bold;"> {title}</h4>
        <ul style="color: #eff1f5; padding-left: 20px; margin-top: 10px; font-size: 0.9rem; line-height: 1.4;">
            {items_html}
        </ul>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# Helper for rendering LeetCode styled tech stack cards
def tech_card(title, items):
    items_html = "".join([f"<li style='margin-bottom:6px;'>{item}</li>" for item in items])
    card_html = f"""
    <div style="
        background-color: #282828;
        border-radius: 8px;
        padding: 20px;
        border-left: 5px solid #8b949e;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        min-height: 180px;
    ">
        <h4 style="color: #eff1f5; margin-top:0; font-size:1.1rem; font-weight:bold;"> {title}</h4>
        <ul style="color: #eff1f5; padding-left: 20px; margin-top: 10px; font-size: 0.9rem; line-height: 1.4;">
            {items_html}
        </ul>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)



# -------------------- FEATURES --------------------

st.header(" Dashboard Features")

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    feature_card("Profile",  [
        "Avatar & Bio",
        "Global Ranking",
        "Reputation Score",
        "Important Social Links"
    ])

with row1_col2:
    feature_card("Question Analytics",  [
        "Difficulty Breakdown",
        "Topic-wise Analysis",
        "Top Strongest Topics",
        "Suggested Practice Areas"
    ])

with row1_col3:
    feature_card("Contest Analytics",  [
        "Contest Rating & Badge",
        "Global Ranking Position",
        "Attended Contest History",
        "Rating Progression Chart"
    ])

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    feature_card("Submission Calendar",  [
        "LeetCode-themed Heatmap",
        "Active Streak Analysis",
        "Submission History Log",
        "Download History as CSV"
    ])

with row2_col2:
    feature_card("AI Insights",  [
        "Interview Readiness Grade",
        "Gemini AI Study Evaluator",
        "Custom Practice Recommendations",
        "Interactive Checklist Goals"
    ])

with row2_col3:
    feature_card("Export Report",  [
        "One-click PDF Generation",
        "Themed Analytics Tables",
        "High-contrast PNG Graphics",
        "Integrated AI Evaluation Report"
    ])

st.divider()    
# -------------------- DASHBOARD PREVIEW --------------------

st.header(" Dashboard Preview")

st.info(
    "Open the pages in the sidebar to view full interactive charts, heatmap calendar, AI feedback, and downloadable report sheets."
)

st.divider()

# -------------------- PROJECT STATS --------------------

st.header("Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Pages", "6")

with c2:
    st.metric("Charts", "8+")

with c3:
    st.metric("Reports", "PDF + CSV")

with c4:
    st.metric("API", "GraphQL")

st.divider()

# -------------------- TECH STACK --------------------

st.header(" Tech Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    tech_card("Python Core",  [
        "Requests (HTTP / GraphQL)",
        "Pandas (Data manipulation)",
        "JSON (Data parsing)"
    ])

with tech_col2:
    tech_card("Visualization",  [
        "Streamlit (App Framework)",
        "Matplotlib (Theme-aware charts)",
        "HTML/CSS (LeetCode card containers)"
    ])

with tech_col3:
    tech_card("APIs & Reports",  [
        "LeetCode GraphQL Endpoints",
        "Google Gemini API (Generative AI)",
        "ReportLab (Themed PDF compilation)"
    ])

st.divider()    

# -------------------- ABOUT --------------------


st.header(" About")

st.write("""
LeetCode Analytics Dashboard helps developers explore public LeetCode profiles through interactive charts, topic-wise analytics, contest insights, GitHub-style submission calendars, AI-generated recommendations, and downloadable PDF reports.

Built using Python, Streamlit, GraphQL, Matplotlib and ReportLab.
""")

st.divider()

# -------------------- FOOTER --------------------

st.caption(
    " LeetCode Analytics Dashboard • Built with Python, Streamlit, GraphQL & Matplotlib"
)

st.caption("Made with ❤️ by Navya Mittal")




    

