import streamlit as st
import os

profile = st.session_state.get("profile")
progress = st.session_state.get("progress")
contests = st.session_state.get("contests")
skills = st.session_state.get("skills")
calendar = st.session_state.get("calendar")

if None in [profile, progress, contests, skills]:
    st.warning(" Please analyze a profile on the Home page first.")
    st.stop()

st.title(" AI Insights & Evaluation")



# ------------------ GEMINI CONFIG ------------------ #

api_key = st.secrets.get("GEMINI_API_KEY", "")
# ------------------ PRE-PROCESS DATA ------------------ #
accepted = progress["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]

# Safe dictionary lookup to fix ordering bug
difficulty_map = {"EASY": 0, "MEDIUM": 0, "HARD": 0}
for item in accepted:
    diff = item.get("difficulty")
    count = item.get("count", 0)
    if diff in difficulty_map:
        difficulty_map[diff] = count

easy = difficulty_map["EASY"]
medium = difficulty_map["MEDIUM"]
hard = difficulty_map["HARD"]
total = easy + medium + hard

# Contest details
contest = contests["data"].get("userContestRanking")
rating = round(contest["rating"]) if contest else 0

# Topic tagging
tag_counts = skills["data"]["matchedUser"].get("tagProblemCounts")
all_topics = []
if tag_counts:
    all_topics = (
        tag_counts.get("fundamental", []) +
        tag_counts.get("intermediate", []) +
        tag_counts.get("advanced", [])
    )
all_topics = [t for t in all_topics if t.get("problemsSolved", 0) > 0]
all_topics.sort(key=lambda x: x.get("problemsSolved", 0), reverse=True)

weak = sorted(all_topics, key=lambda x: x.get("problemsSolved", 0))

# Calendar info
calendar_info = calendar["data"]["matchedUser"].get("userCalendar", {})

# Calculate custom readiness score
score = (easy * 0.15) + (medium * 0.6) + (hard * 1.5)
score = min(round(score), 100)

# Fallback heuristic report generator
def generate_fallback_report():
    strongest_tags = [t['tagName'] for t in all_topics[:2]]
    strongest_str = " and ".join(strongest_tags) if strongest_tags else "various topics"
    weakest_tag = weak[0]['tagName'] if weak else "advanced algorithms"
    
    report = f"""# LeetCode Performance Analytics Report
Generated for user: **{profile['data']['matchedUser']['username']}**

## 1. Executive Summary & Grade
- **Overall Grade:** {"A" if score >= 80 else "B" if score >= 50 else "C"}
- **Interview Readiness Score:** {score}/100
- **Total Problems Solved:** {total} ({easy} Easy, {medium} Medium, {hard} Hard)

Based on your current solved question counts and topic coverage, you have built a solid foundation. However, to be fully ready for competitive software engineering interviews, you should focus on leveling up your problem complexity and increasing consistency.

## 2. Topic Analysis
- **Strong Areas:** You show proficiency in **{strongest_str}**, where you have solved the most problems.
- **Focus Areas:** You should prioritize practice in **{weakest_tag}** to balance your skill profile and fill gaps in knowledge.

## 3. Contest & Speed Evaluation
- **Contest Status:** {"Your contest rating is " + str(rating) + " which shows active participation!" if rating > 0 else "You have not participated in contests yet. Competitive contests are highly recommended to build speed and accuracy under time pressure."}

## 4. 4-Week Study Plan
- **Week 1-2:** Focus on solving 10-15 Medium level problems in **{weakest_tag}**.
- **Week 3-4:** Add 3-5 Hard level problems in your strong areas (**{strongest_str}**) to practice runtime optimizations.

## 5. FAANG Interview Readiness Advice
- **Current Assessment:** { "Ready for initial phone screens, but increase Hard problem count for onsite loops." if hard < 15 else "Strong problem solving profile! Solid chance in tech onsite interviews." }
"""
    return report

# Gemini report generator
from google import genai

def generate_gemini_report(api_key):
    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert technical interviewer and software engineering career coach.

Analyze the following LeetCode profile and generate a detailed professional report.

Profile Details:
- Username: {profile['data']['matchedUser']['username']}
- Global Rank: {profile['data']['matchedUser']['profile'].get('ranking', 'N/A')}
- Reputation: {profile['data']['matchedUser']['profile'].get('reputation', 0)}

Solved Questions:
- Total: {total}
- Easy: {easy}
- Medium: {medium}
- Hard: {hard}

Strongest Topics:
{", ".join([f"{t['tagName']} ({t['problemsSolved']})" for t in all_topics[:5]])}

Weakest Topics:
{", ".join([f"{t['tagName']} ({t['problemsSolved']})" for t in weak[:5]])}

Contest Rating:
{rating}

Calendar:
- Active Days: {calendar_info.get('totalActiveDays',0)}
- Streak: {calendar_info.get('streak',0)}

Generate:

1. Executive Summary
2. Interview Readiness Score (/100)
3. Strengths
4. Weaknesses
5. Personalized 4-week Study Plan
6. FAANG Readiness
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f" {e}\n\n" + generate_fallback_report()


# ------------------ TAB LAYOUT ------------------ #
tab1, tab2, tab3 = st.tabs([" Interview Readiness", " Strengths & Weaknesses", " Detailed Evaluation"])

with tab1:
    st.subheader(" Interview Readiness Score")
    
    col_score1, col_score2 = st.columns([1, 2])
    with col_score1:
        st.metric(
            "Score",
            f"{score}/100",
            help="Heuristic score based on Easy (0.15 pts), Medium (0.6 pts), and Hard (1.5 pts) questions solved."
        )
    with col_score2:
        st.markdown(f"**Readiness Level:** {'Excellent' if score >= 85 else 'Good' if score >= 60 else 'Intermediate' if score >= 35 else 'Beginner'}")
        st.progress(score / 100)

    st.divider()
    
    st.subheader(" Recommended Weekly Goal")
    goals = [
        f"Solve 5 Medium Problems in {weak[0]['tagName'] if weak else 'Recursion'}",
        "Solve 2 Hard Problems in your strongest topic",
        "Participate in 1 Weekly/Biweekly Contest" if rating > 0 else "Participate in your first LeetCode Weekly Contest",
        "Revise code complexity (Big O) for 3 past submissions"
    ]
    for g in goals:
        st.checkbox(g, value=False)

with tab2:
    st.subheader(" Topic Performance Profile")
    
    col_str, col_weak = st.columns(2)
    with col_str:
        st.markdown("### Top Strengths")
        if all_topics:
            for topic in all_topics[:5]:
                st.success(f" **{topic['tagName']}** ({topic['problemsSolved']} solved)")
        else:
            st.info("No topic stats found.")
            
    with col_weak:
        st.markdown("### Improvement Opportunities")
        if weak:
            for topic in weak[:5]:
                st.warning(f" **{topic['tagName']}** ({topic['problemsSolved']} solved)")
        else:
            st.info("No topic stats found.")

with tab3:
    st.subheader(" Detailed Evaluation Report")
    
    if st.button(" Generate AI Evaluation", use_container_width=True):
        with st.spinner("Analyzing profile statistics..."):
            if api_key:
                report_text = generate_gemini_report(api_key)
            else:
                report_text = generate_fallback_report()
            st.session_state["ai_report_text"] = report_text
            
    if "ai_report_text" in st.session_state:
        st.markdown(st.session_state["ai_report_text"])
        
        st.divider()
        
        # Download and Export Report
        st.subheader("📄 Export Report PDF")
        
        from pdf_report import generate_pdf
        
        if st.button("Generate Downloadable PDF", use_container_width=True):
            with st.spinner("Building professional PDF..."):
                generate_pdf(profile, progress, contests, skills, ai_report=st.session_state["ai_report_text"])
                st.success(" PDF report built successfully!")
                
            if os.path.exists("LeetCode_Report.pdf"):
                with open("LeetCode_Report.pdf", "rb") as pdf:
                    st.download_button(
                        "⬇ Download PDF Report",
                        pdf,
                        "LeetCode_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
    else:
        st.info("Click the button above to generate a comprehensive markdown report.")
