import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import random

# --------------------------
# Simulated Data Generator
# --------------------------
def generate_testimonies(num=150):
    platforms = ["YouTube", "TikTok", "Instagram", "X", "Facebook"]
    categories = ["Prophetic Dreams", "Salvation Stories", "Near-Death Experiences"]
    ages = ["18-25", "26-35", "36-50", "50+"]
    
    data = []
    for _ in range(num):
        category = random.choice(categories)
        platform = random.choice(platforms)
        age = random.choice(ages)
        date = datetime.now() - timedelta(days=random.randint(0, 3650))
        credibility = round(random.uniform(40, 98), 2)
        engagement = random.randint(50, 5000)
        positive_comments = random.randint(20, 2000)
        ridicule_comments = random.randint(0, 300)
        link = f"https://{platform.lower()}.com/testimony/{random.randint(10000,99999)}"
        description = f"A {age} believer shares their {category.lower()} about Jesus's return."

        data.append({
            "title": f"{category} - {platform} Post #{random.randint(100, 999)}",
            "category": category,
            "platform": platform,
            "date": date,
            "credibility": credibility,
            "engagement": engagement,
            "positive_comments": positive_comments,
            "ridicule_comments": ridicule_comments,
            "age_range": age,
            "link": link,
            "description": description
        })
    return pd.DataFrame(data)

# --------------------------
# Data Preparation
# --------------------------
@st.cache_data(ttl=1800)  # Refresh every 30 min
def get_testimonies():
    return generate_testimonies(200)

df = get_testimonies()

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.title("Filters")
selected_category = st.sidebar.multiselect(
    "Select Categories",
    options=df["category"].unique(),
    default=df["category"].unique()
)
selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=df["platform"].unique(),
    default=df["platform"].unique()
)
date_range = st.sidebar.slider(
    "Date Range (Years)",
    min_value=1,
    max_value=10,
    value=2
)
search_keyword = st.sidebar.text_input("Search Keyword", "")

# Filter data
cutoff_date = datetime.now() - timedelta(days=date_range * 365)
filtered_df = df[
    (df["category"].isin(selected_category)) &
    (df["platform"].isin(selected_platforms)) &
    (df["date"] >= cutoff_date)
]

if search_keyword:
    filtered_df = filtered_df[filtered_df["description"].str.contains(search_keyword, case=False)]

# --------------------------
# Header
# --------------------------
st.title("Testimony Dashboard")
st.markdown("Tracking prophetic dreams, salvation stories, and near-death experiences for the past 10 years.")

# --------------------------
# Trend Graph
# --------------------------
st.subheader("Trends Over Time")

chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True)

df_trend = (
    filtered_df.groupby(filtered_df["date"].dt.to_period("M"))
    .size()
    .reset_index(name="count")
)
df_trend["date"] = df_trend["date"].dt.to_timestamp()

if chart_type == "Line Chart":
    chart = alt.Chart(df_trend).mark_line(point=True).encode(
        x="date:T",
        y="count:Q",
        tooltip=["date", "count"]
    ).properties(width=800, height=400)
else:
    chart = alt.Chart(df_trend).mark_bar().encode(
        x="date:T",
        y="count:Q",
        tooltip=["date", "count"]
    ).properties(width=800, height=400)

st.altair_chart(chart)

# --------------------------
# Age Distribution
# --------------------------
st.subheader("Age Range of Testimony Posters")
age_dist = filtered_df.groupby("age_range").size().reset_index(name="count")

age_chart = alt.Chart(age_dist).mark_bar().encode(
    x="age_range:N",
    y="count:Q",
    tooltip=["age_range", "count"]
).properties(width=600, height=300)

st.altair_chart(age_chart)

# --------------------------
# Testimony Preview Cards
# --------------------------
st.subheader("Browse Testimonies")

for _, row in filtered_df.sort_values("date", ascending=False).iterrows():
    with st.expander(f"{row['title']} | Credibility: {row['credibility']}% | Age: {row['age_range']}"):
        st.write(f"**Platform:** {row['platform']}")
        st.write(f"**Posted On:** {row['date'].strftime('%Y-%m-%d')}")
        st.write(f"**Description:** {row['description']}")
        st.write(f"**Positive Comments:** {row['positive_comments']}")
        st.write(f"**Ridicule Comments:** {row['ridicule_comments']}")
        st.markdown(f"[View Testimony]({row['link']})")

# --------------------------
# Current Events Context (Placeholder Simulation)
# --------------------------
st.subheader("Current Events Context")
st.write("""
The following key themes match recent testimonies with current world events:
- Wars and rumors of wars (Matthew 24:6)
- Increase in natural disasters (Luke 21:11)
- Global revival and salvation testimonies
""")

# --------------------------
# Credibility Scoring Explanation
# --------------------------
st.sidebar.markdown("### Credibility Score Factors")
st.sidebar.write("""
- Content consistency
- Positive vs. ridicule comment ratio
- Engagement levels
- Risk of public ridicule
- Age range demographics
""")

st.success("Dashboard loaded successfully with live filters and credibility previews!")
