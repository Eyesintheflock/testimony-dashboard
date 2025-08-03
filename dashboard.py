import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import time
import pydeck as pdk
from scraping import scrape_youtube_testimonies, scrape_reddit_testimonies, scrape_tiktok_testimonies, scrape_persecution_data

st.set_page_config(page_title="Testimony Dashboard (Real-Time)", layout="wide")

# ======================
# DATA CACHING
# ======================
@st.cache_data(ttl=1800)  # Refresh every 30 minutes
def load_testimonies():
    youtube_data = scrape_youtube_testimonies()
    reddit_data = scrape_reddit_testimonies()
    tiktok_data = scrape_tiktok_testimonies()
    all_data = youtube_data + reddit_data + tiktok_data
    return pd.DataFrame(all_data)

@st.cache_data(ttl=86400)  # Refresh every 24 hours
def load_persecution_data():
    persecution_data = scrape_persecution_data()
    return pd.DataFrame(persecution_data)

testimonies_df = load_testimonies()
persecution_df = load_persecution_data()

st.title("📊 Testimony Dashboard (Real-Time)")

# ======================
# FILTER CONTROLS
# ======================
platforms = st.multiselect(
    "Filter by Platform",
    options=testimonies_df['platform'].unique(),
    default=list(testimonies_df['platform'].unique())
)
believers_only = st.checkbox("Show Only Believers", value=False)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]
if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]

# ======================
# TESTIMONIES PER PLATFORM
# ======================
st.subheader("Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")
chart = alt.Chart(testimony_counts).mark_bar().encode(
    x=alt.X("platform:N", title="Platform"),
    y=alt.Y("count:Q", title="Number of Testimonies"),
    tooltip=["platform", "count"]
)
st.altair_chart(chart, use_container_width=True)

# ======================
# BELIEVER VS NON-BELIEVER
# ======================
st.subheader("Believer vs Non-Believer Comparison")
belief_counts = testimonies_df.groupby(["platform", "is_believer"]).size().reset_index(name="count")
belief_chart = alt.Chart(belief_counts).mark_bar().encode(
    x="platform",
    y="count",
    color="is_believer:N",
    tooltip=["platform", "is_believer", "count"]
)
st.altair_chart(belief_chart, use_container_width=True)

# ======================
# AGE DISTRIBUTION
# ======================
st.subheader("Age Distribution of Testimonies")
age_counts = testimonies_df.groupby("age_range").size().reset_index(name="count")
age_chart = alt.Chart(age_counts).mark_bar().encode(
    x="age_range",
    y="count",
    tooltip=["age_range", "count"]
)
st.altair_chart(age_chart, use_container_width=True)

# ======================
# GLOBAL PERSECUTION MAP
# ======================
st.subheader("Global Christian Persecution Cases")
if not persecution_df.empty:
    persecution_df["latitude"] = np.random.uniform(-50, 60, size=len(persecution_df))  # Replace with real geo-coordinates if available
    persecution_df["longitude"] = np.random.uniform(-120, 120, size=len(persecution_df))

    st.map(persecution_df.rename(columns={"latitude": "lat", "longitude": "lon"}))

    persecution_chart = alt.Chart(persecution_df).mark_bar().encode(
        x="country",
        y="cases",
        tooltip=["country", "cases", "source_url"]
    )
    st.altair_chart(persecution_chart, use_container_width=True)

    for _, row in persecution_df.iterrows():
        st.markdown(f"**{row['country']}** – {row['cases']} cases [View Source]({row['source_url']})")

# ======================
# TESTIMONY LIST (REAL LINKS)
# ======================
st.subheader("Latest Testimonies")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.markdown(f"- **Platform:** {row['platform']}")
    st.markdown(f"- **Age Range:** {row['age_range']}")
    st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
    st.markdown(f"- **Description:** {row['description']}")
    st.markdown(f"- **Categories:** {', '.join(row['prophecy_categories'])}")
    st.markdown(f"[🔗 View Testimony]({row['source_url']})", unsafe_allow_html=True)
    st.markdown("---")
