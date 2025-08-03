import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# Simulated data generator
def generate_data():
    dates = pd.date_range(datetime.now() - timedelta(days=365 * 10), datetime.now(), freq='M')
    data = {
        'date': np.tile(dates, 3),
        'category': np.repeat(['Prophetic Visions', 'Salvation Stories', 'Near-Death Experiences'], len(dates)),
        'count': np.random.randint(10, 200, len(dates) * 3),
    }
    return pd.DataFrame(data)

# Simulated testimony list with descriptions and credibility
def generate_testimonies():
    return [
        {
            "title": "Dream of Jesus Appearing in the Clouds",
            "description": "A woman describes a vivid dream of Jesus calling believers home.",
            "source": "YouTube",
            "credibility": 87,
            "url": "https://youtube.com/example1"
        },
        {
            "title": "Former Atheist Finds Christ",
            "description": "A man shares his testimony of salvation after years of disbelief.",
            "source": "TikTok",
            "credibility": 92,
            "url": "https://tiktok.com/example2"
        },
        {
            "title": "Near-Death Experience Confirms Heaven",
            "description": "A testimony of a person clinically dead for 3 minutes who saw Jesus.",
            "source": "Instagram",
            "credibility": 95,
            "url": "https://instagram.com/example3"
        }
    ]

st.set_page_config(page_title="Testimony Dashboard", layout="wide")

st.title("📊 Testimony Dashboard")
st.write("Track prophetic visions, salvation stories, and near-death experiences over the last 10 years.")

# Generate data
df = generate_data()
testimonies = generate_testimonies()

# Sidebar filters
st.sidebar.header("Filters")
selected_category = st.sidebar.multiselect(
    "Select Categories",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filter data
filtered_df = df[df['category'].isin(selected_category)]

# Altair Chart
st.subheader("📈 Testimonies Over Time")
chart = (
    alt.Chart(filtered_df)
    .mark_line(point=True)
    .encode(
        x="date:T",
        y="count:Q",
        color="category:N",
        tooltip=["date:T", "category:N", "count:Q"]
    )
    .interactive()
)
st.altair_chart(chart, use_container_width=True)

# Testimony Previews
st.subheader("📝 Testimony Previews")
for t in testimonies:
    with st.expander(f"{t['title']} (Credibility: {t['credibility']}%)"):
        st.write(f"**Description:** {t['description']}")
        st.write(f"**Source:** {t['source']}")
        st.markdown(f"[Watch/Testimony Link]({t['url']})")

st.caption("Data auto-refresh planned every 30 minutes when connected to live feeds.")
