import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import time

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ----------------------------------------
# Data Loading Functions
# ----------------------------------------
@st.cache_data(ttl=1800)  # Refresh every 30 mins
def load_testimonies():
    return pd.read_csv("testimonies.csv")

@st.cache_data(ttl=1800)
def load_persecution_data():
    return pd.read_csv("persecution_data.csv")

testimonies_df = load_testimonies()
persecution_data = load_persecution_data()

# ----------------------------------------
# Page Title
# ----------------------------------------
st.title("Global Testimony Dashboard with Real-Time Updates")

# ----------------------------------------
# Filters
# ----------------------------------------
platforms = st.multiselect(
    "Filter by Platform",
    options=testimonies_df['platform'].unique(),
    default=list(testimonies_df['platform'].unique())
)
believers_only = st.checkbox("Show Only Believers", value=False)
show_labels = st.checkbox("Show data labels on charts", value=True)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]
if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]

# ----------------------------------------
# Testimonies Per Platform Chart
# ----------------------------------------
st.subheader("Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")

platform_chart = alt.Chart(testimony_counts).mark_bar().encode(
    x=alt.X("platform:N", title="Platform"),
    y=alt.Y("count:Q", title="Number of Testimonies"),
    color="platform:N",
    tooltip=["platform", "count"]
)

if show_labels:
    text_labels = alt.Chart(testimony_counts).mark_text(dy=-10).encode(
        x="platform:N",
        y="count:Q",
        text=alt.Text("count:Q"),
        color="platform:N"
    )
    st.altair_chart(platform_chart + text_labels, use_container_width=True)
else:
    st.altair_chart(platform_chart, use_container_width=True)

# ----------------------------------------
# Believers vs Non-Believers Credibility
# ----------------------------------------
st.subheader("Believers vs. Non-Believers Credibility Comparison")
believer_comparison = filtered_df.groupby(["platform", "is_believer"])["credibility_score"].mean().reset_index(name="avg_credibility")

credibility_chart = alt.Chart(believer_comparison).mark_line(point=True).encode(
    x="platform:N",
    y="avg_credibility:Q",
    color="is_believer:N",
    tooltip=["platform", "avg_credibility", "is_believer"]
)

if show_labels:
    text_labels = credibility_chart.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.Text("avg_credibility:Q", format=".1f"),
        color="is_believer:N"
    )
    st.altair_chart(credibility_chart + text_labels, use_container_width=True)
else:
    st.altair_chart(credibility_chart, use_container_width=True)

# ----------------------------------------
# Global Persecution Graph
# ----------------------------------------
st.subheader("Global Christian Persecution Cases")
persecution_chart = alt.Chart(persecution_data).mark_line(point=True).encode(
    x="year:O",
    y="cases:Q",
    color="region:N",
    tooltip=["year", "cases", "region"]
)

if show_labels:
    text_labels = persecution_chart.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.Text("cases:Q"),
        color="region:N"
    )
    st.altair_chart(persecution_chart + text_labels, use_container_width=True)
else:
    st.altair_chart(persecution_chart, use_container_width=True)

# ----------------------------------------
# Global Testimony Map
# ----------------------------------------
st.subheader("Global Map of Testimonies")
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
    st.map(filtered_df[["latitude", "longitude"]], zoom=1)
else:
    st.warning("No geolocation data available for testimonies.")

# ----------------------------------------
# Testimony Listings
# ----------------------------------------
st.subheader("Latest Testimonies")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.markdown(f"- **Platform:** {row['platform']}")
    st.markdown(f"- **Age Range:** {row['age_range']}")
    st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
    st.markdown(f"- **Description:** {row['description']}")
    st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)
    st.markdown("---")

# ----------------------------------------
# Comparison: Non-Believers vs Believers Count
# ----------------------------------------
st.subheader("Testimony Count Comparison (Believers vs. Non-Believers)")
belief_comparison = filtered_df.groupby(["platform", "is_believer"]).size().reset_index(name="count")

belief_chart = alt.Chart(belief_comparison).mark_bar().encode(
    x="platform:N",
    y="count:Q",
    color="is_believer:N",
    tooltip=["platform", "is_believer", "count"]
)
st.altair_chart(belief_chart, use_container_width=True)

# ----------------------------------------
# Refresh Time
# ----------------------------------------
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
