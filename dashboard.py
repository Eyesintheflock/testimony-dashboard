import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Testimony Trends", layout="wide")

st.title("📊 Testimony & Vision Dashboard")
st.markdown("Track trends in prophetic dreams, visions, salvation stories, and near-death experiences across platforms.")

# Simulated data
months = pd.date_range(end=pd.Timestamp.today(), periods=24, freq="M").strftime("%b %Y")
testimonies = np.random.randint(20, 120, size=24)
salvations = np.random.randint(10, 80, size=24)
nde = np.random.randint(5, 30, size=24)

df = pd.DataFrame({
    "Month": months,
    "Prophetic Visions": testimonies,
    "Salvation Stories": salvations,
    "Near-Death Experiences": nde
})

# Line chart
st.line_chart(df.set_index("Month"))

# Sidebar filter (expandable)
with st.sidebar:
    st.header("Filters")
    st.multiselect("Platforms", ["YouTube", "TikTok", "X", "Instagram", "Reddit"], default=["YouTube", "TikTok"])
    st.slider("Time Range (months)", 1, 24, 12)

st.success("This is just a demo with simulated data. Live social media feeds coming soon!")
