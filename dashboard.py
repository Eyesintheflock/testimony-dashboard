import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data(ttl=1800)  # Refresh every 30 mins
def load_testimonies():
    return pd.read_csv("testimonies.csv")

testimonies_df = load_testimonies()

st.title("Testimony Dashboard (Real-Time & Interactive)")
st.write("Explore prophetic dreams, visions, near-death experiences, salvation testimonies, and Christian persecution trends.")

# ======================
# FILTERS
# ======================
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect(
    "Filter by Platform", 
    options=testimonies_df["platform"].unique(), 
    default=list(testimonies_df["platform"].unique())
)
believers_only = st.sidebar.checkbox("Show Only Believers", value=False)
non_believers_only = st.sidebar.checkbox("Show Only Non-Believers", value=False)

filtered_df = testimonies_df[testimonies_df["platform"].isin(platforms)]

if believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == True]
elif non_believers_only:
    filtered_df = filtered_df[filtered_df["is_believer"] == False]

# ======================
# GRAPH: TESTIMONIES PER PLATFORM
# ======================
st.subheader("Testimonies Per Platform")
testimony_counts = filtered_df.groupby("platform").size().reset_index(name="count")
platform_chart = alt.Chart(testimony_counts).mark_bar().encode(
    x=alt.X("platform", sort="-y"),
    y="count",
    tooltip=["platform", "count"]
).properties(width=700)
st.altair_chart(platform_chart, use_container_width=True)

# ======================
# GRAPH: BELIEVER VS NON-BELIEVER PERCENTAGE
# ======================
st.subheader("Believer vs Non-Believer Testimonies")
believer_counts = testimonies_df["is_believer"].value_counts().reset_index()
believer_counts.columns = ["Believer", "Count"]
believer_counts["Believer"] = believer_counts["Believer"].map({True: "Believers", False: "Non-Believers"})

believer_chart = alt.Chart(believer_counts).mark_arc().encode(
    theta="Count",
    color="Believer",
    tooltip=["Believer", "Count"]
)
st.altair_chart(believer_chart, use_container_width=True)

# ======================
# GRAPH: GLOBAL PERSECUTION CASES (SIMULATED)
# ======================
st.subheader("Global Christian Persecution Cases (Simulated Data)")
years = list(range(2015, datetime.now().year + 1))
persecution_data = pd.DataFrame({
    "year": years,
    "cases": np.random.randint(1000, 5000, size=len(years)),
    "percent_reported_online": np.random.uniform(30, 80, size=len(years))
})

persecution_chart = alt.Chart(persecution_data).mark_line(point=True).encode(
    x="year",
    y="cases",
    tooltip=["year", "cases"]
).properties(title="Persecution Cases per Year")
st.altair_chart(persecution_chart, use_container_width=True)

st.write("Percentage of persecution cases reported online is simulated below.")
perc_chart = alt.Chart(persecution_data).mark_line(color="red").encode(
    x="year",
    y="percent_reported_online",
    tooltip=["year", "percent_reported_online"]
)
st.altair_chart(perc_chart, use_container_width=True)

# ======================
# TESTIMONY LIST
# ======================
st.subheader("Latest Testimonies")
for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.markdown(f"- **Platform:** {row['platform']}")
    st.markdown(f"- **Age Range:** {row['age_range']}")
    st.markdown(f"- **Credibility Score:** {row['credibility_score']}%")
    st.markdown(f"- **Description:** {row['description']}")
    st.markdown(f"[View Testimony]({row['source_url']})", unsafe_allow_html=True)
    st.markdown("---")

# ======================
# FOOTER
# ======================
st.write("Data refreshes every 30 minutes. All links provided are user-submitted or collected via API integrations.")
