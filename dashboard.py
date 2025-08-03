import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
from scraping import scrape_youtube_testimonies, scrape_reddit_testimonies, scrape_tiktok_testimonies, scrape_persecution_data, analyze_comment_sentiment

# ===========================
# PAGE CONFIG
# ===========================
st.set_page_config(page_title="Global Testimony Dashboard", layout="wide")

# ===========================
# API KEYS (from GitHub Secrets or .streamlit/secrets.toml)
# ===========================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
REDDIT_CLIENT_ID = st.secrets["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = st.secrets["REDDIT_CLIENT_SECRET"]
OPENCAGE_API_KEY = st.secrets["OPENCAGE_API_KEY"]

# ===========================
# DATA LOADING
# ===========================
@st.cache_data(ttl=1800)
def load_data():
    # Real-time scrape
    youtube_data = scrape_youtube_testimonies(YOUTUBE_API_KEY, OPENCAGE_API_KEY)
    reddit_data = scrape_reddit_testimonies(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, "testimony-dashboard", OPENCAGE_API_KEY)
    tiktok_data = scrape_tiktok_testimonies(OPENCAGE_API_KEY)
    persecution_data = scrape_persecution_data(OPENCAGE_API_KEY)

    # Combine testimonies
    all_data = youtube_data + reddit_data + tiktok_data

    for testimony in all_data:
        sentiment_score = analyze_comment_sentiment(testimony["comments"])
        base_score = testimony.get("credibility_score", 50)
        sentiment_impact = sentiment_score * 20
        adjusted_score = min(100, max(0, base_score + sentiment_impact))
        testimony["credibility_breakdown"] = {
            "base_score": base_score,
            "sentiment_impact": sentiment_impact,
            "final_score": adjusted_score
        }
        testimony["credibility_score"] = adjusted_score

    return pd.DataFrame(all_data), pd.DataFrame(persecution_data)

testimonies_df, persecution_df = load_data()

st.title("🌍 Global Testimony Dashboard")
st.write("Live data for testimonies, near-death experiences, and Christian persecution worldwide.")

# ===========================
# FILTERS
# ===========================
platforms = st.multiselect("Filter by Platform", options=testimonies_df["platform"].unique(), default=list(testimonies_df["platform"].unique()))
believers_only = st.checkbox("Show Only Believers", value=False)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]
if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]

# ===========================
# TESTIMONY PER PLATFORM
# ===========================
st.subheader("📊 Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")
chart = alt.Chart(testimony_counts).mark_bar().encode(
    x="platform",
    y="count",
    tooltip=["platform", "count"]
)
st.altair_chart(chart, use_container_width=True)

# ===========================
# BELIEVER VS NON-BELIEVER
# ===========================
st.subheader("🙏 Believer vs Non-Believer")
belief_counts = testimonies_df.groupby("is_believer").size().reset_index(name="count")
belief_counts["label"] = belief_counts["is_believer"].map({True: "Believers", False: "Non-Believers"})
belief_chart = alt.Chart(belief_counts).mark_bar().encode(
    x="label",
    y="count",
    tooltip=["label", "count"]
)
st.altair_chart(belief_chart, use_container_width=True)

# ===========================
# MAP VISUALIZATION
# ===========================
st.subheader("🗺 Testimonies & Persecution Map")
if not filtered_df.empty:
    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.5)

    testimony_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position="[longitude, latitude]",
        get_radius=500000,
        get_color=[0, 128, 255],
        pickable=True
    )

    persecution_layer = pdk.Layer(
        "ScatterplotLayer",
        data=persecution_df,
        get_position="[longitude, latitude]",
        get_radius=700000,
        get_color=[255, 0, 0],
        pickable=True
    )

    tooltip = {
        "html": "<b>{platform}</b><br>{title}<br>Credibility: {credibility_score}%<br><a href='{source_url}' target='_blank'>View Testimony</a>",
        "style": {"color": "white"}
    }

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[testimony_layer, persecution_layer],
        tooltip=tooltip
    ))
else:
    st.warning("No testimonies match selected filters.")

# ===========================
# TESTIMONY LIST WITH CREDIBILITY BREAKDOWN
# ===========================
st.subheader("📜 Testimonies")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.markdown(f"- **Platform:** {row['platform']}")
    st.markdown(f"- **Age Range:** {row['age_range']}")
    st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
    st.markdown(f"- **Description:** {row['description']}")
    st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)

    with st.expander("🔍 View Credibility Breakdown"):
        breakdown = row["credibility_breakdown"]
        st.write(f"- Base Score: {breakdown['base_score']}%")
        st.write(f"- Sentiment Impact: {breakdown['sentiment_impact']:.2f}")
        st.write(f"- Final Score: {breakdown['final_score']}%")

    st.markdown("---")

# ===========================
# PERSECUTION DATA
# ===========================
st.subheader("🚨 Christian Persecution Data")
for _, row in persecution_df.iterrows():
    st.markdown(f"- **Country:** {row['country']}")
    st.markdown(f"[Read More]({row['source_url']})")
    st.markdown("---")
