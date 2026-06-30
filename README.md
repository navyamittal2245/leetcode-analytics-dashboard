# 📊 LeetCode Analytics Dashboard

A modern Streamlit dashboard that analyzes any public LeetCode profile and presents detailed analytics through interactive charts, AI-powered insights, submission heatmaps, contest statistics, and downloadable PDF reports.

---

##  Live Demo

🔗 https://leetcode-analytics-dashboard-npjqzuknrsaya4gk9xqfyd.streamlit.app/

---

##  Features

###  Profile Analytics
- User profile information
- Global ranking
- Reputation score
- Education & profession (if available)
- Social profile links

###  Question Analytics
- Problems solved by difficulty
- Topic-wise distribution
- Strongest topics
- Weakest topics
- Submission statistics
- Interactive visualizations

###  Contest Analytics
- Contest rating
- Global ranking
- Rating history
- Contest participation statistics

###  Submission Calendar
- GitHub-style submission heatmap
- Daily submission counts
- Active streak analysis
- CSV export support

###  AI Insights
- Interview readiness score
- Strengths & weaknesses analysis
- Personalized study recommendations
- AI-generated evaluation report using Gemini

###  Report Generation
- Download professional PDF reports
- Includes profile statistics
- Charts and analytics
- AI-generated evaluation

---

##  Screenshots



##  Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Data Source
- LeetCode GraphQL API

### Libraries
- Pandas
- Matplotlib
- Requests
- ReportLab
- Google Gemini API

---

##  Project Structure

```
leetcode-analytics-dashboard/
│
├── app.py
├── fetch_data.py
├── charts.py
├── heatmap.py
├── pdf_report.py
├── requirements.txt
│
├── pages/
│   ├── 1_Profile.py
│   ├── 2_Question_Analytics.py
│   ├── 3_Contest_Analytics.py
│   ├── 4_AI_Insights.py
│   └── 5_Submission_Calendar.py
│
└── .streamlit/
    └── config.toml
```

---

##  Installation

Clone the repository

```bash
git clone https://github.com/navyamittal2245/leetcode-analytics-dashboard.git
```

Move into the project directory

```bash
cd leetcode-analytics-dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

##  Environment Variables

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

The dashboard works without Gemini, but AI-generated insights require a valid API key.

---

##  Dashboard Overview

The dashboard includes:

- Home Page
- Profile Analysis
- Question Analytics
- Contest Analytics
- Submission Calendar
- AI Insights & Evaluation

---

##  Future Improvements

- User authentication
- Compare multiple LeetCode profiles
- Company-wise problem analysis
- Difficulty trend prediction
- More AI-powered recommendations
- Additional visualization options

---

##  Author

**Navya Mittal**

GitHub: https://github.com/navyamittal2245

---

##  Support

If you found this project useful, consider giving it a ⭐ on GitHub!
