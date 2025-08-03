import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import pydeck as pdk
from scraping import scrape_youtube_testimonies, scrape_reddit_testimonies, scrape_tiktok_testimonies, scrape_persecution_data

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ======================
# REFRESH INTERVAL
# ======================
@st.cache_data(ttl=1800)  # Refresh every 30 min
def load_testimonies():
    yt_data = scrape_youtube_testimonies()
    reddit_data = scrape_reddit_testimonies()
    tiktok_data = scrape_tiktok_testimonies()
    return pd.DataFrame(yt_data + reddit_data + tiktok_data)

@st.cache_data(ttl=1800)
def load_persecution_data():
    return pd.DataFrame(scrape_persecution_data())

testimonies_df = load_testimonies()
persecution_df = load_persecution_data()

# ======================
# TITLE
# ======================
st.title("Testimony Dashboard with Real Links, Credibility, and Prophecy Correlation")

# ======================
# FILTERS
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
# TESTIMONY GRAPH
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
# BELIEVER VS NON-BELIEVER
# ======================
st.subheader("Believers vs Non-Believers")
believer_counts = testimonies_df.groupby("is_believer").size().reset_index(name="count")
believer_chart = alt.Chart(believer_counts).mark_arc().encode(
    theta="count",
    color="is_believer",
    tooltip=["is_believer", "count"]
)
st.altair_chart(believer_chart, use_container_width=True)

# ======================
# TESTIMONY MAP
# ======================
st.subheader("Testimony Map (Global)")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1.5),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position="[longitude, latitude]",
            get_color="[200, 30, 0, 160]",
            get_radius=500000,
            pickable=True
        )
    ],
    tooltip={"text": "{title}\nPlatform: {platform}\nCredibility: {credibility_score}%"}
))

# ======================
# PERSECUTION DATA
# ======================
st.subheader("Global Christian Persecution Cases")
persecution_chart = alt.Chart(persecution_df).mark_bar().encode(
    x="country",
    y="cases",
    tooltip=["country", "cases"]
).properties(width=800)
st.altair_chart(persecution_chart, use_container_width=True)

# ======================
# PROPHECY CORRELATION
# ======================
st.subheader("Prophecy Correlation Analysis")

prophecy_keywords = {
    "Rapture": ["rapture", "caught up", "taken up"],
    "Second Coming": ["second coming", "Jesus return", "Christ's return"],
    "End Times": ["end times", "tribulation", "apocalypse", "mark of the beast"],
    "Visions & Dreams": ["vision", "dream", "prophetic word"],
}

def analyze_prophecy_correlation(df):
    results = {k: 0 for k in prophecy_keywords}
    for _, row in df.iterrows():
        description = row["description"].lower()
        for category, keywords in prophecy_keywords.items():
            if any(keyword in description for keyword in keywords):
                results[category] += 1
    return pd.DataFrame(list(results.items()), columns=["Prophecy Category", "Count"])

prophecy_df = analyze_prophecy_correlation(filtered_df)

prophecy_chart = alt.Chart(prophecy_df).mark_bar().encode(
    x="Prophecy Category",
    y="Count",
    tooltip=["Prophecy Category", "Count"]
)
st.altair_chart(prophecy_chart, use_container_width=True)

# ======================
# TESTIMONY LIST WITH CREDIBILITY TOOLTIP
# ======================
st.subheader("Latest Testimonies")

for _, row in filtered_df.iterrows():
    credibility_breakdown = f"""
    **Credibility Breakdown:**
    - Posting Frequency: ~{round(row['credibility_score'] * 0.4)}%
    - Sentiment Score: ~{round(row['credibility_score'] * 0.3)}%
    - Ridicule Factor: ~{round(row['credibility_score'] * 0.2)}%
    - Platform Weight: ~{round(row['credibility_score'] * 0.1)}%
    """
    with st.expander(f"📌 {row['title']}"):
        st.markdown(f"- **Platform:** {row['platform']}")
        st.markdown(f"- **Age Range:** {row['age_range']}")
        st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
        st.markdown(credibility_breakdown)
        st.markdown(f"- **Description:** {row['description']}")
        st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)
        st.markdown("---")
