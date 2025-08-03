import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# ---------------------------
# Credibility Scoring Logic
# ---------------------------
def calculate_credibility(support_comments, ridicule_comments, reposts, consistent_content):
    base_score = 50
    base_score += min(30, support_comments // 10)
    base_score -= min(20, ridicule_comments // 10)
    base_score += min(10, reposts // 5)
    if consistent_content:
        base_score += 10
    return max(0, min(100, base_score))

# ---------------------------
# Simulated Testimony Data
# ---------------------------
def generate_testimonies():
    return [
        {
            "title": "Dream of Jesus Appearing in the Clouds",
            "description": "A woman describes a vivid dream of Jesus calling believers home.",
            "source": "YouTube",
            "credibility": calculate_credibility(150, 30, 10, True),
            "url": "https://youtube.com/watch?v=example1",
            "events_relation": "Tied to the increase in global unrest and natural disasters."
        },
        {
            "title": "Former Atheist Finds Christ",
            "description": "A man shares his testimony of salvation after years of disbelief.",
            "source": "TikTok",
            "credibility": calculate_credibility(300, 50, 0, True),
            "url": "https://www.tiktok.com/@exampleuser/video/123456",
            "events_relation": "Connects to rising revival movements and personal transformation stories."
        },
        {
            "title": "Near-Death Experience Confirms Heaven",
            "description": "A testimony of a person clinically dead for 3 minutes who saw Jesus.",
            "source": "Instagram",
            "credibility": calculate_credibility(500, 20, 5, False),
            "url": "https://instagram.com/reel/example123",
            "events_relation": "Related to the growing interest in afterlife studies and biblical alignment."
        },
        {
            "title": "Prophetic Word on Global Economy",
            "description": "A preacher shares a vision of financial collapse followed by spiritual awakening.",
            "source": "X (Twitter)",
            "credibility": calculate_credibility(200, 40, 15, True),
            "url": "https://twitter.com/exampleuser/status/123456",
            "events_relation": "Matches recent market instability and concerns about end-times economics."
        }
    ]

# ---------------------------
# Testimony Trends Data
# ---------------------------
def generate_data():
    dates = pd.date_range(datetime.now() - timedelta(days=365 * 10), datetime.now(), freq='M')
    data = {
        'date': np.tile(dates, 3),
        'category': np.repeat(['Prophetic Visions', 'Salvation Stories', 'Near-Death Experiences'], len(dates)),
        'count': np.random.randint(5, 150, len(dates) * 3),
    }
    return pd.DataFrame(data)

# ---------------------------
# Streamlit Layout
# ---------------------------
st.set_page_config(page_title="Testimony Dashboard", layout="wide")

st.title("📊 Testimony Dashboard")
st.write("Track prophetic visions, salvation stories, and near-death experiences over the last 10 years, updated in near real-time.")

df = generate_data()
testimonies = generate_testimonies()

# Sidebar filters
st.sidebar.header("Filters")
selected_category = st.sidebar.multiselect(
    "Select Categories",
    options=df['category'].unique(),
    default=df['category'].unique()
)

view_mode = st.sidebar.radio("View Mode", ["Monthly", "Yearly"])

# Filter and aggregate
filtered_df = df[df['category'].isin(selected_category)]
if view_mode == "Yearly":
    filtered_df["year"] = filtered_df["date"].dt.year
    chart_data = filtered_df.groupby(["year", "category"], as_index=False)["count"].sum()
    x_axis = "year:O"
else:
    filtered_df["month"] = filtered_df["date"].dt.to_period("M").astype(str)
    chart_data = filtered_df.groupby(["month", "category"], as_index=False)["count"].sum()
    x_axis = "month:O"

# ---------------------------
# Trend Chart
# ---------------------------
st.subheader("📈 Testimony Trends")
chart = (
    alt.Chart(chart_data)
    .mark_bar()
    .encode(
        x=alt.X(x_axis, title="Date"),
        y=alt.Y("count:Q", title="Number of Testimonies"),
        color="category:N",
        tooltip=["category:N", "count:Q"]
    )
    .properties(width=900)
    .interactive()
)
st.altair_chart(chart, use_container_width=True)

# ---------------------------
# Testimony Browser
# ---------------------------
st.subheader("📝 Testimony Browser")
for t in testimonies:
    color = "🟢" if t['credibility'] > 80 else "🟡" if t['credibility'] > 50 else "🔴"
    with st.expander(f"{color} {t['title']} (Credibility: {t['credibility']}%)"):
        st.write(f"**Description:** {t['description']}")
        st.write(f"**Source Platform:** {t['source']}")
        st.write(f"**Relation to Current Events:** {t['events_relation']}")
        st.markdown(f"[🔗 View Testimony Directly]({t['url']})")

st.caption("Data refresh planned every 30 minutes when integrated with live APIs.")
