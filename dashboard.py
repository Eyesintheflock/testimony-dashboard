import streamlit as st
import pandas as pd
import numpy as np

# Simulated data from 2015 to present
years = pd.date_range(start="2015-01-01", end="2025-07-01", freq="MS")
data = {
    "Date": years,
    "Prophetic Visions": np.random.poisson(15, len(years)).cumsum(),
    "Salvation Stories": np.random.poisson(25, len(years)).cumsum(),
    "Near-Death Experiences": np.random.poisson(10, len(years)).cumsum(),
    "Credibility Score": np.clip(np.random.normal(75, 10, len(years)), 0, 100)
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Testimony Trends Dashboard", layout="wide")
st.title("📊 Testimonies & Visions Trend Dashboard")
st.markdown("Tracking prophetic dreams, salvation stories, and NDEs from the last 10 years")

# Date Range Filter
date_range = st.slider(
    "Select Date Range",
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date(),
    value=(df["Date"].min().date(), df["Date"].max().date())
)
filtered = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

# Trend Charts
st.subheader("📈 Trends Over Time")
st.line_chart(filtered.set_index("Date")[["Prophetic Visions", "Salvation Stories", "Near-Death Experiences"]])

st.subheader("🔍 Credibility Score Over Time")
st.line_chart(filtered.set_index("Date")[["Credibility Score"]])

# Leaderboard Section
st.subheader("🏆 Top Trending Testimonials (Simulated)")
leaderboard = pd.DataFrame({
    "Platform": ["YouTube", "TikTok", "X", "Instagram", "Reddit"],
    "Testimonies Tracked": [1220, 935, 764, 543, 488],
    "Avg Credibility": [89, 84, 76, 72, 70]
})
st.dataframe(leaderboard)

st.markdown("This is a **simulated preview**. Live data integration from YouTube, TikTok, and others is coming soon.")
