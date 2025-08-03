import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# ---- TITLE ----
st.title("📊 Testimony Dashboard")
st.write("Track prophetic visions, salvation stories, and near-death experiences across major platforms (YouTube, X, TikTok, Instagram).")

# ---- DATE RANGE ----
st.sidebar.header("Filters")
years = st.sidebar.slider("Select years to view", 1, 10, 2)
start_date = datetime.now() - timedelta(days=365 * years)

# ---- SIMULATED DATA GENERATION ----
np.random.seed(42)
dates = pd.date_range(start=start_date, end=datetime.now(), freq="W")
data = pd.DataFrame({
    "date": dates,
    "prophetic_visions": np.random.randint(20, 200, len(dates)),
    "salvation_stories": np.random.randint(30, 250, len(dates)),
    "near_death_experiences": np.random.randint(10, 100, len(dates))
})

# Add credibility ranking based on comments & shares (simulated)
data["credibility_score"] = np.random.uniform(0.5, 5.0, len(dates))

# ---- CHARTS ----
st.subheader("📈 Trends Over Time")
trend_chart = alt.Chart(data).transform_fold(
    ["prophetic_visions", "salvation_stories", "near_death_experiences"],
    as_=["category", "count"]
).mark_line().encode(
    x="date:T",
    y="count:Q",
    color="category:N",
    tooltip=["date:T", "category:N", "count:Q"]
).interactive()

st.altair_chart(trend_chart, use_container_width=True)

# ---- CREDIBILITY RANKINGS ----
st.subheader("🏆 Credibility Rankings")
cred_chart = alt.Chart(data).mark_bar().encode(
    x="date:T",
    y="credibility_score:Q",
    tooltip=["date:T", "credibility_score:Q"]
)
st.altair_chart(cred_chart, use_container_width=True)

# ---- METRICS ----
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Prophetic Visions", int(data["prophetic_visions"].sum()))
col2.metric("Total Salvation Stories", int(data["salvation_stories"].sum()))
col3.metric("Total Near-Death Experiences", int(data["near_death_experiences"].sum()))

st.write("✅ This dashboard is using **simulated data**. In the next version, it will connect to real-time platform APIs (YouTube, TikTok, X, Instagram).")
