import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from datetime import datetime
from scraping import scrape_youtube_testimonies, scrape_reddit_testimonies, scrape_tiktok_testimonies, scrape_persecution_data

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data(ttl=1800)  # Refresh every 30 min
def load_testimonies():
    data = scrape_youtube_testimonies() + scrape_reddit_testimonies() + scrape_tiktok_testimonies()
    return pd.DataFrame(data)

@st.cache_data(ttl=1800)
def load_persecution_data():
    return pd.DataFrame(scrape_persecution_data())

testimonies_df = load_testimonies()
persecution_df = load_persecution_data()

st.title("Testimony Dashboard with Real Links & Prophecy Insights")

# ======================
# FILTER CONTROLS
# ======================
platforms = st.multiselect("Filter by Platform", options=testimonies_df['platform'].unique(), default=list(testimonies_df['platform'].unique()))
believers_only = st.checkbox("Show Only Believers", value=False)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]
if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]

# ======================
# TESTIMONIES PER PLATFORM (GRAPH)
# ======================
st.subheader("Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")
chart = alt.Chart(testimony_counts).mark_bar().encode(
    x="platform",
    y="count",
    tooltip=["platform", "count"]
)
st.altair_chart(chart, use_container_width=True)

# ======================
# GLOBAL MAP OF TESTIMONIES
# ======================
st.subheader("Global Map of Testimonies")
if not filtered_df.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1.5, pitch=0),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered_df,
                get_position="[longitude, latitude]",
                get_color="[200, 30, 0, 160]",
                get_radius=500000,
            ),
        ],
    ))

# ======================
# PROPHECY CATEGORY DISTRIBUTION
# ======================
st.subheader("Prophecy Category Distribution")
prophecy_expanded = filtered_df.explode("prophecy_categories")
prophecy_counts = prophecy_expanded["prophecy_categories"].value_counts().reset_index()
prophecy_counts.columns = ["Category", "Count"]

if not prophecy_counts.empty:
    prophecy_chart = alt.Chart(prophecy_counts).mark_bar().encode(
        x="Category",
        y="Count",
        tooltip=["Category", "Count"]
    )
    st.altair_chart(prophecy_chart, use_container_width=True)

# ======================
# PERSECUTION DATA (GLOBAL)
# ======================
st.subheader("Global Christian Persecution Cases")
if not persecution_df.empty:
    persecution_chart = alt.Chart(persecution_df).mark_bar().encode(
        x="country",
        y="cases",
        tooltip=["country", "cases"]
    )
    st.altair_chart(persecution_chart, use_container_width=True)

    st.write("### Percentage of Online Persecution Stories")
    total_cases = persecution_df["cases"].sum()
    online_cases_estimated = int(total_cases * 0.35)  # Assume ~35% of cases are shared online
    st.write(f"Estimated Online Cases: **{online_cases_estimated}** / {total_cases} (~35%)")

# ======================
# TESTIMONY LIST WITH CLICKABLE LINKS
# ======================
st.subheader("Latest Testimonies")
if filtered_df.empty:
    st.warning("No testimonies match your filters.")
else:
    for _, row in filtered_df.iterrows():
        st.markdown(f"### {row['title']}")
        st.markdown(f"- **Platform:** {row['platform']}")
        st.markdown(f"- **Age Range:** {row['age_range']}")
        st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
        st.markdown(f"- **Prophecy Categories:** {', '.join(row['prophecy_categories'])}")
        st.markdown(f"- **Description:** {row['description']}")
        st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)
        st.markdown("---")
