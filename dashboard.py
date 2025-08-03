import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from scraping import scrape_youtube_testimonies, scrape_reddit_testimonies, scrape_tiktok_testimonies, scrape_persecution_data

# ===========================
# PAGE CONFIG
# ===========================
st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ===========================
# API KEYS & CONFIG
# ===========================
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
REDDIT_CLIENT_ID = st.secrets["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = st.secrets["REDDIT_CLIENT_SECRET"]
REDDIT_USER_AGENT = "testimony-dashboard"

# ===========================
# AUTO REFRESH SETUP (30 min)
# ===========================
if "last_update" not in st.session_state or datetime.now() - st.session_state.last_update > timedelta(minutes=30):
    st.session_state.last_update = datetime.now()

    youtube_data = scrape_youtube_testimonies(YOUTUBE_API_KEY, max_results=8)
    reddit_data = scrape_reddit_testimonies(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, limit=8)
    tiktok_data = scrape_tiktok_testimonies()
    persecution_data = scrape_persecution_data()

    all_testimonies = youtube_data + reddit_data + tiktok_data
    st.session_state.testimonies_df = pd.DataFrame(all_testimonies)
    st.session_state.persecution_df = pd.DataFrame(persecution_data)

# ===========================
# LOAD DATA
# ===========================
testimonies_df = st.session_state.testimonies_df
persecution_df = st.session_state.persecution_df

# ===========================
# TITLE
# ===========================
st.title("Testimony Dashboard (Real-Time)")
st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')} | Auto-refresh every 30 minutes")

# ===========================
# FILTERS
# ===========================
platforms = st.multiselect(
    "Filter by Platform",
    options=testimonies_df["platform"].unique(),
    default=list(testimonies_df["platform"].unique())
)

believers_only = st.checkbox("Show Only Believers", value=False)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]
if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]

# ===========================
# GRAPH: TESTIMONIES PER PLATFORM
# ===========================
st.subheader("Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")

chart = alt.Chart(testimony_counts).mark_bar().encode(
    x=alt.X("platform:N", title="Platform"),
    y=alt.Y("count:Q", title="Number of Testimonies"),
    tooltip=["platform", "count"]
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

# ===========================
# GRAPH: BELIEVER VS NON-BELIEVER
# ===========================
st.subheader("Believers vs Non-Believers")
belief_counts = filtered_df.groupby("is_believer").size().reset_index(name="count")
belief_counts["is_believer"] = belief_counts["is_believer"].map({True: "Believers", False: "Non-Believers"})

belief_chart = alt.Chart(belief_counts).mark_arc(innerRadius=50).encode(
    theta="count",
    color="is_believer",
    tooltip=["is_believer", "count"]
)
st.altair_chart(belief_chart, use_container_width=True)

# ===========================
# GLOBAL MAP OF TESTIMONIES
# ===========================
if "latitude" in testimonies_df.columns and "longitude" in testimonies_df.columns:
    st.subheader("Global Map of Testimonies")
    st.map(filtered_df[["latitude", "longitude"]])

# ===========================
# TESTIMONY LIST WITH CLICKABLE LINKS
# ===========================
st.subheader("Latest Testimonies")

for _, row in filtered_df.iterrows():
    with st.expander(f"📌 {row['title']}"):
        st.markdown(f"- **Platform:** {row['platform']}")
        st.markdown(f"- **Age Range:** {row['age_range']}")
        st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
        st.markdown(f"- **Description:** {row['description']}")
        st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)

        if isinstance(row.get("comments"), list):
            st.markdown("**Top Comments:**")
            for comment in row["comments"][:5]:
                st.write(f"💬 {comment}")

        st.markdown("---")

# ===========================
# GLOBAL CHRISTIAN PERSECUTION DATA
# ===========================
st.header("Global Christian Persecution Cases")

if not persecution_df.empty:
    # Map of persecution
    if "latitude" in persecution_df.columns and "longitude" in persecution_df.columns:
        st.map(persecution_df[["latitude", "longitude"]])

    # Persecution stats by country
    st.subheader("Persecution by Country")
    country_counts = persecution_df.groupby("country").size().reset_index(name="count").sort_values("count", ascending=False)

    bar_chart = alt.Chart(country_counts).mark_bar().encode(
        x=alt.X("country:N", title="Country", sort="-y"),
        y=alt.Y("count:Q", title="Number of Cases"),
        tooltip=["country", "count"]
    ).properties(height=400)

    st.altair_chart(bar_chart, use_container_width=True)

    # Percentage of persecution stories with sources
    st.subheader("Verified Persecution Reports")
    if "source_url" in persecution_df.columns:
        verified_cases = persecution_df[persecution_df["source_url"].notnull()]
        total_cases = len(persecution_df)
        verified_percentage = (len(verified_cases) / total_cases) * 100 if total_cases > 0 else 0

        st.write(f"✅ **{verified_percentage:.2f}% of reported persecution cases include a verified online story**")

        # Show table of verified persecution stories
        st.markdown("### Verified Cases with Links")
        for _, row in verified_cases.iterrows():
            st.markdown(f"- {row['country']}: [Read Story]({row['source_url']})")

else:
    st.warning("No persecution data available at this time.")
