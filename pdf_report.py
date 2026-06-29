from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from charts import (
    difficulty_chart,
    difficulty_pie_chart,
    contest_history_chart,
    topic_chart
)
import matplotlib.pyplot as plt

import os

styles = getSampleStyleSheet()


def generate_pdf(profile, progress, contests, skills, ai_report=None):

    doc = SimpleDocTemplate("LeetCode_Report.pdf")

    story = []

    try:
        # ---------------- PROFILE DATA ---------------- #

        user = profile["data"]["matchedUser"]
        info = user["profile"]

        # ---------------- QUESTION DATA ---------------- #

        accepted = progress["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]

        # Safely map counts using a dictionary to prevent ordering swap bugs, case-sensitivity issues
        difficulty_map = {"Easy": 0, "Medium": 0, "Hard": 0}
        for item in accepted:
            diff = item.get("difficulty", "").title()
            count = item.get("count", 0)
            if diff in difficulty_map:
                difficulty_map[diff] = count

        easy = difficulty_map["Easy"]
        medium = difficulty_map["Medium"]
        hard = difficulty_map["Hard"]

        total = easy + medium + hard

        difficulties = ["Easy", "Medium", "Hard"]
        counts = [easy, medium, hard]

        # ---------------- CREATE CHARTS ---------------- #

        bar_fig = difficulty_chart(difficulties, counts)
        pie_fig = difficulty_pie_chart(difficulties, counts)

        bar_fig.savefig(
            "difficulty_bar.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.close(bar_fig)

        pie_fig.savefig(
            "difficulty_pie.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.close(pie_fig)

        # ---------------- TITLE ---------------- #

        story.append(
            Paragraph(
                "LeetCode Analytics Report",
                styles["Title"]
            )
        )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        # ---------------- PROFILE ---------------- #

        story.append(
            Paragraph(
                "<b>Profile</b>",
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                f"Username : {user['username']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Name : {info['realName']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Country : {info['countryName']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Ranking : {info['ranking']:,}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Reputation : {info['reputation']}",
                styles["Normal"]
            )
        )

        if info["school"]:
            story.append(
                Paragraph(
                    f"School : {info['school']}",
                    styles["Normal"]
                )
            )

        if info["company"]:
            story.append(
                Paragraph(
                    f"Company : {info['company']}",
                    styles["Normal"]
                )
            )

        if info["jobTitle"]:
            story.append(
                Paragraph(
                    f"Job Title : {info['jobTitle']}",
                    styles["Normal"]
                )
            )

        story.append(PageBreak())

        # ---------------- QUESTION ANALYTICS ---------------- #

        story.append(
            Paragraph(
                "<b>Question Analytics</b>",
                styles["Heading1"]
            )
        )

        data = [
            ["Difficulty", "Solved"],
            ["Easy", easy],
            ["Medium", medium],
            ["Hard", hard],
            ["Total", total]
        ]

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#282828")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#ffa116")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(table)

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        story.append(
            Image(
                "difficulty_bar.png",
                width=420,
                height=260
            )
        )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        story.append(
            Image(
                "difficulty_pie.png",
                width=320,
                height=320
            )
        )

        story.append(PageBreak())

        # ---------------- CONTEST ANALYTICS ---------------- #

        contest = contests["data"]["userContestRanking"]
        history = contests["data"]["userContestRankingHistory"]

        if contest is not None:

            story.append(
                Paragraph(
                    "<b>Contest Analytics</b>",
                    styles["Heading1"]
                )
            )

            contest_data = [
                ["Metric", "Value"],
                ["Rating", round(contest["rating"])],
                ["Global Rank", f"{contest['globalRanking']:,}"],
                ["Contests Attended", contest["attendedContestsCount"]],
                ["Top Percentage", f"{contest['topPercentage']:.2f}%"]
            ]

            contest_table = Table(contest_data)
            # Style Contest Table
            contest_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#282828")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#ffa116")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]))

            story.append(contest_table)

            story.append(Paragraph("<br/>", styles["Normal"]))

            contest_fig = contest_history_chart(history)

            contest_fig.savefig(
                "contest_chart.png",
                dpi=300,
                bbox_inches="tight"
            )
            plt.close(contest_fig)

            story.append(
                Image(
                    "contest_chart.png",
                    width=450,
                    height=260
                )
            )

        # ---------------- TOPIC ANALYSIS ---------------- #

        story.append(PageBreak())

        story.append(
            Paragraph(
                "<b>Topic-wise Analysis</b>",
                styles["Heading1"]
            )
        )

        topics = skills["data"]["matchedUser"]["tagProblemCounts"]

        all_topics = (
            topics["fundamental"] +
            topics["intermediate"] +
            topics["advanced"]
        )

        all_topics = [
            topic
            for topic in all_topics
            if topic["problemsSolved"] > 0
        ]

        all_topics.sort(
            key=lambda x: x["problemsSolved"],
            reverse=True
        )

        top_topics = all_topics[:10]

        topic_names = []
        solved = []

        for topic in top_topics:
            topic_names.append(topic["tagName"])
            solved.append(topic["problemsSolved"])

        topic_fig = topic_chart(
            topic_names,
            solved
        )

        topic_fig.savefig(
            "topic_chart.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.close(topic_fig)

        story.append(
            Image(
                "topic_chart.png",
                width=450,
                height=260
            )
        )

        story.append(Paragraph("<br/>", styles["Normal"]))

        topic_data = [["Topic", "Problems Solved"]]

        for topic in top_topics:
            topic_data.append([
                topic["tagName"],
                topic["problemsSolved"]
            ])

        topic_table = Table(topic_data)

        topic_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#282828")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#ffa116")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f9f9f9")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(topic_table)

        story.append(Paragraph("<br/>", styles["Normal"]))

        story.append(
            Paragraph(
                "<b>Strongest Topics</b>",
                styles["Heading2"]
            )
        )

        for topic in top_topics[:5]:
            story.append(
                Paragraph(
                    f"• {topic['tagName']} ({topic['problemsSolved']} solved)",
                    styles["Normal"]
                )
            )

        story.append(Paragraph("<br/>", styles["Normal"]))

        story.append(
            Paragraph(
                "<b>Needs More Practice</b>",
                styles["Heading2"]
            )
        )

        weak_topics = sorted(
            all_topics,
            key=lambda x: x["problemsSolved"]
        )[:5]

        for topic in weak_topics:
            story.append(
                Paragraph(
                    f"• {topic['tagName']} ({topic['problemsSolved']} solved)",
                    styles["Normal"]
                )
            )

        # ---------------- AI PERSONALIZED REPORT ---------------- #
        if ai_report:
            story.append(PageBreak())
            story.append(
                Paragraph(
                    "<b>AI Personalized Report Insights</b>",
                    styles["Heading1"]
                )
            )
            story.append(Paragraph("<br/>", styles["Normal"]))
            
            # Simple markdown block parser for ReportLab PDF flowables
            for line in ai_report.split("\n"):
                line = line.strip()
                if not line:
                    story.append(Paragraph("<br/>", styles["Normal"]))
                    continue
                
                # Check markdown headings
                if line.startswith("# "):
                    story.append(Paragraph(f"<b>{line[2:]}</b>", styles["Heading1"]))
                elif line.startswith("## "):
                    story.append(Paragraph(f"<b>{line[3:]}</b>", styles["Heading2"]))
                elif line.startswith("### "):
                    story.append(Paragraph(f"<b>{line[4:]}</b>", styles["Heading3"]))
                elif line.startswith("- ") or line.startswith("* "):
                    story.append(Paragraph(f"• {line[2:]}", styles["Normal"]))
                else:
                    story.append(Paragraph(line, styles["Normal"]))

        # ---------------- BUILD PDF ---------------- #

        doc.build(story)

    finally:
        # ---------------- CLEANUP ---------------- #
        for file in [
            "difficulty_bar.png",
            "difficulty_pie.png",
            "contest_chart.png",
            "topic_chart.png"
        ]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception:
                    pass
  