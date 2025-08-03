import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# -----------------------------
# DATA GENERATION (SIMULATION)
# -----------------------------
platforms = ["YouTube", "TikTok", "X", "Instagram", "Reddit"]
age_ranges = ["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]
topics = ["Prophetic Vision", "End Times", "Near-Death Experience", "Salvation Testimony"]

def generate_testimonies(num=100):
    testimonies = []
    for _ in range(num):
        platform = random.choice(platforms)
        title = f"{random.choice(topics)} #{random.randint(1, 500)}"
        age_range = random.choice(age_ranges)
        credibility_score = random.randint(50, 100)
        is_believer = random.choice([True, False])
        timestamp = datetime.now() - timedelta(days=random.randint(0, 365*10))
        description = f"A testimony about {title.lower()} from {platform}."
        url = f"https://{platform.lower()}.com/watch?v={random.randint(10000,99999)}" if platform == "YouTube" else f"https://{platform.lower()}.com/post/{random.randint(10000,99999)}"
        
        testimonies.append({
            "title": title,
            "platform": platform,
            "age_range": age_range,
            "credibility_score": credibility_score,
            "is_believer": is_believer,
            "description": description,
            "source_url": url,
            "timestamp": timestamp
        })
    return testimonies

testimonies_data = generate_testimonies(200)

# Simulated persecution data
def generate_persecution_data(years=10):
    data = []
    current_year = datetime.now().year
    for year in range(current_year - years, current_year + 1):
        cases = random.randint(5000, 30000)
        online_percentage = round(random.uniform(5, 25), 2)
        data.append({
            "year": year,
            "cases": cases,
            "online_percentage": online_percentage,
            "links": [f"https://news.example.com/persecution/{year}/{i}" for i in range(1, 4)]
        })
    return data

persecution_data = generate_persecution_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")
selected_platform = st.sidebar.multiselect("Platform", platforms, default=platforms)
selected_topic = st.sidebar.multiselect("Topic", topics, default=topics)
selected_age = st.sidebar.multiselect("Age Range", age_ranges, default=age_ranges)
min_credibility = st.sidebar.slider("Minimum Credibility", 50, 100, 70)
believer_filter = st.sidebar.selectbox("Believer/Non-Believer", ["All", "Believers", "Non-Believers"])

# Filter testimonies
filtered_testimonies = [
    t for t in testimonies_data
    if t["platform"] in selected_platform
    and any(topic in t["title"] for topic in selected_topic)
    and t["age_range"] in selected_age
    and t["credibility_score"] >= min_credibility
    and (believer_filter == "All" or (believer_filter == "Believers" and t["is_believer"]) or (believer_filter == "Non-Believers" and not t["is_believer"]))
]

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Testimony Dashboard")
st.markdown("Tracking prophetic visions, dreams, salvation stories, near-death experiences, and global Christian persecution.")

# -----------------------------
# GRAPHS
# -----------------------------

# Testimonies over time
df_testimonies = pd.DataFrame([{
    "Date": t["timestamp"].date(),
    "Platform": t["platform"]
} for t in filtered_testimonies])

if not df_testimonies.empty:
    timeline = df_testimonies.groupby(["Date", "Platform"]).size().reset_index(name="Count")
    line_chart = alt.Chart(timeline).mark_line().encode(
        x="Date:T",
        y="Count:Q",
        color="Platform:N"
    ).properties(title="Testimonies Over Time", height=300)
    st.altair_chart(line_chart, use_container_width=True)

# Believers vs Non-Believers
believers_count = sum(1 for t in filtered_testimonies if t["is_believer"])
non_believers_count = len(filtered_testimonies) - believers_count

st.subheader("Believers vs Non-Believers")
st.bar_chart(pd.DataFrame({
    "Count": [believers_count, non_believers_count]
}, index=["Believers", "Non-Believers"]))

# Persecution cases
df_persecution = pd.DataFrame(persecution_data)
persecution_chart = alt.Chart(df_persecution).mark_bar().encode(
    x="year:O",
    y="cases:Q",
    tooltip=["cases", "online_percentage"]
).properties(title="Global Christian Persecution Cases", height=300)
st.altair_chart(persecution_chart, use_container_width=True)

# -----------------------------
# TESTIMONY LIST
# -----------------------------
st.subheader("📜 Testimonies")

if filtered_testimonies:
    for testimony in filtered_testimonies:
        with st.expander(f"{testimony['title']} ({testimony['platform']})"):
            st.write(f"**Description:** {testimony['description']}")
            st.write(f"**Age Range:** {testimony['age_range']}")
            st.write(f"**Credibility Score:** {testimony['credibility_score']}%")
            st.write(f"**Believer:** {'Yes' if testimony['is_believer'] else 'No'}")
            st.write(f"**Date:** {testimony['timestamp'].strftime('%Y-%m-%d')}")

            st.markdown(f"[🔗 View Testimony]({testimony['source_url']})", unsafe_allow_html=True)
            if "youtube.com" in testimony["source_url"]:
                st.video(testimony["source_url"])
else:
    st.warning("No testimonies match the selected filters.")

# -----------------------------
# PERSECUTION LINKS
# -----------------------------
st.subheader("🌎 Christian Persecution Links")
for entry in persecution_data:
    st.write(f"**{entry['year']}** - {entry['cases']} cases reported ({entry['online_percentage']}% found online)")
    for link in entry["links"]:
        st.markdown(f"[Read More]({link})", unsafe_allow_html=True)
    st.markdown("---")
