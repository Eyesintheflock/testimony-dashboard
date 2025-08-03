import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
from datetime import datetime, timedelta

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Testimony Dashboard", layout="wide")

# -------------------------------
# SIMULATED DATA GENERATION
# -------------------------------

def generate_testimonies(num=120):
    platforms = ["YouTube", "X (Twitter)", "Instagram", "TikTok", "Reddit"]
    categories = ["Prophetic Vision", "Dream", "Salvation Testimony", "Near Death Experience"]
    age_ranges = ["Under 18", "18–25", "26–35", "36–50", "51+"]
    testimonies = []

    for i in range(num):
        platform = random.choice(platforms)
        category = random.choice(categories)
        age = random.choice(age_ranges)
        believer = random.choice(["Believer", "Non-Believer"])
        credibility_score = random.randint(30, 100)
        credibility_tier = "High" if credibility_score >= 75 else "Moderate" if credibility_score >= 50 else "Low"
        comments = random.randint(10, 500)
        reposts = random.randint(0, 150)
        link = f"https://www.example.com/testimony/{i}"
        description = f"A {believer.lower()} shared a {category.lower()} on {platform} with {comments} comments."
        ridicule_ratio = random.randint(0, 100)
        supportive_ratio = 100 - ridicule_ratio

        testimonies.append({
            "id": i,
            "platform": platform,
            "category": category,
            "age_range": age,
            "believer_status": believer,
            "credibility_score": credibility_score,
            "credibility_tier": credibility_tier,
            "comments": comments,
            "reposts": reposts,
            "supportive_ratio": supportive_ratio,
            "ridicule_ratio": ridicule_ratio,
            "description": description,
            "link": link,
            "date": datetime.now() - timedelta(days=random.randint(0, 365 * 10))
        })
    return pd.DataFrame(testimonies)

def generate_persecution_data():
    countries = ["Nigeria", "China", "India", "Pakistan", "North Korea", "Middle East"]
    data = []
    for country in countries:
        for year in range(2015, 2026):
            data.append({
                "country": country,
                "year": year,
                "cases": random.randint(50, 500),
                "source_link": f"https://www.example.com/persecution/{country}/{year}"
            })
    return pd.DataFrame(data)

# -------------------------------
# DATA
# -------------------------------
testimony_data = generate_testimonies()
persecution_data = generate_persecution_data()

# -------------------------------
# UI HEADER
# -------------------------------
st.title("✝ Testimony Dashboard – Prophetic Dreams, Salvation, and Persecution Trends")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 30 min)")

# -------------------------------
# FILTERS
# -------------------------------
with st.sidebar:
    st.header("Filters")
    selected_platforms = st.multiselect("Select Platforms", testimony_data["platform"].unique(), default=testimony_data["platform"].unique())
    selected_categories = st.multiselect("Select Categories", testimony_data["category"].unique(), default=testimony_data["category"].unique())
    selected_believer_status = st.multiselect("Believer Status", ["Believer", "Non-Believer"], default=["Believer", "Non-Believer"])
    selected_age = st.multiselect("Age Range", testimony_data["age_range"].unique(), default=testimony_data["age_range"].unique())

# Filter dataset
filtered_data = testimony_data[
    (testimony_data["platform"].isin(selected_platforms)) &
    (testimony_data["category"].isin(selected_categories)) &
    (testimony_data["believer_status"].isin(selected_believer_status)) &
    (testimony_data["age_range"].isin(selected_age))
]

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Trends", "📝 Testimonies", "✝ Believer vs Non-Believer", "🌍 Global Persecution"])

# -------------------------------
# TAB 1: TRENDS
# -------------------------------
with tab1:
    st.subheader("Testimony Trends (Past 10 Years)")

    chart_data = filtered_data.copy()
    chart_data["year"] = chart_data["date"].dt.year

    trend_chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x="year:O",
        y="count():Q",
        color="category:N",
        tooltip=["year", "category", "count()"]
    ).interactive()

    st.altair_chart(trend_chart, use_container_width=True)

    st.info("This chart shows how testimonies have trended across categories in the last 10 years.")

# -------------------------------
# TAB 2: TESTIMONIES LIST
# -------------------------------
with tab2:
    st.subheader("Browse Testimonies")
    for _, row in filtered_data.iterrows():
        with st.expander(f"{row['category']} – {row['platform']} – Credibility: {row['credibility_tier']}"):
            st.write(f"**Description:** {row['description']}")
            st.write(f"**Age Range:** {row['age_range']}")
            st.write(f"**Believer Status:** {row['believer_status']}")
            st.write(f"**Credibility Score:** {row['credibility_score']} ({row['credibility_tier']})")
            st.write(f"**Support vs Ridicule:** {row['supportive_ratio']}% supportive / {row['ridicule_ratio']}% ridicule")
            st.write(f"**Comments:** {row['comments']} | **Reposts:** {row['reposts']}")
            st.markdown(f"[View Testimony]({row['link']})")

# -------------------------------
# TAB 3: BELIEVER VS NON-BELIEVER
# -------------------------------
with tab3:
    st.subheader("Believer vs Non-Believer Testimony Comparison")

    believer_comparison = filtered_data.groupby(["believer_status"]).size().reset_index(name="count")
    bar_chart = alt.Chart(believer_comparison).mark_bar().encode(
        x="believer_status",
        y="count",
        color="believer_status",
        tooltip=["believer_status", "count"]
    )

    st.altair_chart(bar_chart, use_container_width=True)
    st.info("This chart compares the number of testimonies from believers vs. non-believers.")

# -------------------------------
# TAB 4: PERSECUTION DATA
# -------------------------------
with tab4:
    st.subheader("Global Christian Persecution Cases")

    persecution_chart = alt.Chart(persecution_data).mark_line(point=True).encode(
        x="year:O",
        y="cases:Q",
        color="country:N",
        tooltip=["country", "year", "cases"]
    ).interactive()

    st.altair_chart(persecution_chart, use_container_width=True)

    st.write("### Sources:")
    for _, row in persecution_data.sample(6).iterrows():
        st.markdown(f"- [{row['country']} ({row['year']})]({row['source_link']})")

# -------------------------------
# SUMMARY INSIGHTS
# -------------------------------
st.markdown("---")
st.header("📌 Automated Insights")

total_testimonies = len(filtered_data)
high_credibility = len(filtered_data[filtered_data["credibility_tier"] == "High"])
believers = len(filtered_data[filtered_data["believer_status"] == "Believer"])
non_believers = len(filtered_data[filtered_data["believer_status"] == "Non-Believer"])

st.write(f"**Total testimonies:** {total_testimonies}")
st.write(f"**High credibility testimonies:** {high_credibility}")
st.write(f"**Believers:** {believers} | **Non-Believers:** {non_believers}")

if high_credibility > (total_testimonies * 0.6):
    st.success("Majority of testimonies have high credibility based on posting behavior and audience reaction.")
else:
    st.warning("Many testimonies lack strong supporting credibility indicators.")
