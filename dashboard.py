import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# Simulated Data Generator
def generate_testimony_data():
    platforms = ["YouTube", "TikTok", "Instagram", "X (Twitter)"]
    categories = ["Prophetic Vision", "Salvation Testimony", "Near-Death Experience"]
    testimonies = []
    for i in range(30):
        category = random.choice(categories)
        score = random.randint(30, 100)
        testimonies.append({
            "title": f"{category} #{i+1}",
            "platform": random.choice(platforms),
            "description": f"A {category.lower()} shared recently, gaining traction on social media.",
            "credibility": score,
            "link": f"https://example.com/testimony/{i+1}",
            "score_breakdown": {
                "Content Consistency": random.randint(5, 25),
                "Engagement Sentiment": random.randint(10, 30),
                "Repost Verification": random.randint(5, 20),
                "Historical Accuracy": random.randint(0, 15),
                "Risk Factor": random.randint(0, 10),
            }
        })
    return testimonies

testimonies = generate_testimony_data()

# Sidebar filters
st.sidebar.title("Filters")
selected_category = st.sidebar.multiselect("Select Category", ["Prophetic Vision", "Salvation Testimony", "Near-Death Experience"], default=["Prophetic Vision"])
min_credibility = st.sidebar.slider("Minimum Credibility Score", 0, 100, 50)

# Filtered testimonies
filtered_testimonies = [t for t in testimonies if t["credibility"] >= min_credibility and t["title"].split()[0] in selected_category]

# Dashboard Title
st.title("Testimony Dashboard (Demo)")
st.markdown("Tracking prophetic visions, salvations, and near-death experiences with credibility scoring.")

# Graph (Trend Simulation)
st.subheader("Trend of Testimonies (Past 10 Years)")
years = list(range(2015, 2025))
data = {
    "Prophetic Visions": np.random.randint(10, 100, len(years)),
    "Salvation Testimonies": np.random.randint(10, 100, len(years)),
    "Near-Death Experiences": np.random.randint(10, 100, len(years)),
}
df = pd.DataFrame(data, index=years)
st.line_chart(df)

# Testimony List
st.subheader("Testimonies")
for t in filtered_testimonies:
    with st.expander(f"{t['title']} | {t['platform']} | Credibility: {t['credibility']}"):
        st.write(t["description"])
        st.markdown(f"[View Source]({t['link']})")
        st.write("### Credibility Breakdown")
        st.json(t["score_breakdown"])
