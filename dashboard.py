import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import random
from datetime import datetime, timedelta

# ===============================
# CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Testimony Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# DATA SIMULATION
# ===============================

PLATFORMS = ["YouTube", "TikTok", "Instagram", "X (Twitter)", "Reddit"]
CATEGORIES = ["Prophetic Vision", "Near Death Experience", "Salvation Story"]
AGE_RANGES = ["Under 18", "18-25", "26-35", "36-50", "51+"]
MOCK_LINKS = {
    "YouTube": "https://www.youtube.com/results?search_query=",
    "TikTok": "https://www.tiktok.com/search?q=",
    "Instagram": "https://www.instagram.com/explore/tags/",
    "X (Twitter)": "https://twitter.com/search?q=",
    "Reddit": "https://www.reddit.com/search/?q="
}

# Generate a credibility score based on multiple weighted factors
def calculate_credibility(post_frequency, ridicule_factor, supportive_comments):
    score = (supportive_comments * 0.5) + ((1 - ridicule_factor) * 0.3) + (post_frequency * 0.2)
    return round(score * 100, 2)

# Generate simulated testimony data
def generate_testimonies(n=100):
    data = []
    now = datetime.now()

    for _ in range(n):
        platform = random.choice(PLATFORMS)
        category = random.choice(CATEGORIES)
        age_range = random.choice(AGE_RANGES)
        is_believer = random.choice([True, False])

        # credibility scoring factors
        post_frequency = random.uniform(0, 1)
        ridicule_factor = random.uniform(0, 1)
        supportive_comments = random.uniform(0, 1)

        credibility = calculate_credibility(post_frequency, ridicule_factor, supportive_comments)

        # timestamp for trend analysis
        timestamp = now - timedelta(days=random.randint(0, 365 * 10))

        # description and link
        description = f"{'Believer' if is_believer else 'Non-believer'} shares {category.lower()} on {platform}"
        link = MOCK_LINKS[platform] + category.replace(" ", "+")

        data.append({
            "platform": platform,
            "category": category,
            "description": description,
            "link": link,
            "credibility": credibility,
            "age_range": age_range,
            "is_believer": is_believer,
            "timestamp": timestamp
        })

    return pd.DataFrame(data)

# Generate simulated persecution data
def generate_persecution_data(years=10):
    now = datetime.now()
    data = []
    for i in range(years * 12):  # monthly data
        date = now - timedelta(days=i * 30)
        documented_cases = random.randint(200, 3000)
        online_cases = random.randint(int(documented_cases * 0.1), int(documented_cases * 0.6))

        # mock link to online persecution reports
        link = f"https://www.opendoors.org/en-US/persecution-reports/{date.year}/{date.month:02d}"

        data.append({
            "month": date.strftime("%Y-%m"),
            "documented_cases": documented_cases,
            "online_cases": online_cases,
            "link": link
        })

    df = pd.DataFrame(data)
    return df.sort_values("month")

# Initial data generation
df = generate_testimonies(300)
persecution_df = generate_persecution_data(10)

# ===============================
# SIDEBAR CONTROLS
# ===============================
st.sidebar.header("Filters")
selected_category = st.sidebar.multiselect("Select Category", CATEGORIES, default=CATEGORIES)
selected_platform = st.sidebar.multiselect("Select Platform", PLATFORMS, default=PLATFORMS)
selected_believer = st.sidebar.selectbox("Believer Filter", ["All", "Believers", "Non-Believers"])
selected_age = st.sidebar.multiselect("Select Age Range", AGE_RANGES, default=AGE_RANGES)

# Filter data based on selections
filtered_df = df[
    (df["category"].isin(selected_category)) &
    (df["platform"].isin(selected_platform)) &
    (df["age_range"].isin(selected_age))
]

if selected_believer == "Believers":
    filtered_df = filtered_df[filtered_df["is_believer"] == True]
elif selected_believer == "Non-Believers":
    filtered_df = filtered_df[filtered_df["is_believer"] == False]

# ===============================
# METRICS ROW
# ===============================
st.title("📊 Testimony Dashboard")

total_testimonies = len(filtered_df)
avg_credibility = filtered_df["credibility"].mean() if not filtered_df.empty else 0
believers = len(filtered_df[filtered_df["is_believer"] == True])
non_believers = len(filtered_df[filtered_df["is_believer"] == False])

col1, col2, col3 = st.columns(3)
col1.metric("Total Testimonies", total_testimonies)
col2.metric("Avg. Credibility Score", f"{avg_credibility:.2f}")
col3.metric("Believers vs Non-Believers", f"{believers}:{non_believers}")

# ===============================
# VISUALIZATION 1: TREND OVER TIME
# ===============================
st.subheader("📈 Testimonies Over Time (Last 10 Years)")

time_df = filtered_df.copy()
time_df["month"] = time_df["timestamp"].dt.to_period("M").astype(str)
trend = time_df.groupby("month").size().reset_index(name="count")

line_chart = alt.Chart(trend).mark_line(point=True).encode(
    x="month:T",
    y="count:Q",
    tooltip=["month", "count"]
).properties(
    height=400,
    width=900
)

st.altair_chart(line_chart, use_container_width=True)

# ===============================
# VISUALIZATION 2: BELIEVERS VS NON-BELIEVERS
# ===============================
st.subheader("🙏 Believers vs Non-Believers by Platform")

believer_data = filtered_df.groupby(["platform", "is_believer"]).size().reset_index(name="count")

bar_chart = alt.Chart(believer_data).mark_bar().encode(
    x="platform:N",
    y="count:Q",
    color=alt.Color("is_believer:N", legend=alt.Legend(title="Believer")),
    tooltip=["platform", "is_believer", "count"]
).properties(
    height=400,
    width=900
)

st.altair_chart(bar_chart, use_container_width=True)

# ===============================
# VISUALIZATION 3: AGE RANGE DISTRIBUTION
# ===============================
st.subheader("📊 Testimonies by Age Range")

age_data = filtered_df.groupby("age_range").size().reset_index(name="count")

age_chart = alt.Chart(age_data).mark_bar().encode(
    x="age_range:N",
    y="count:Q",
    color="age_range:N",
    tooltip=["age_range", "count"]
).properties(
    height=400,
    width=900
)

st.altair_chart(age_chart, use_container_width=True)

# ===============================
# VISUALIZATION 4: GLOBAL PERSECUTION DATA
# ===============================
st.subheader("🌍 Global Christian Persecution Cases (10-Year Trend)")

persecution_chart = alt.Chart(persecution_df).transform_fold(
    ["documented_cases", "online_cases"],
    as_=["type", "cases"]
).mark_line(point=True).encode(
    x="month:T",
    y="cases:Q",
    color=alt.Color("type:N", legend=alt.Legend(title="Case Type")),
    tooltip=["month", "type", "cases"]
).properties(
    height=400,
    width=900
)

st.altair_chart(persecution_chart, use_container_width=True)

# Persecution percentage
latest_month = persecution_df.iloc[-1]
persecution_percentage = (latest_month["online_cases"] / latest_month["documented_cases"]) * 100
st.metric("Online Persecution Stories (Latest Month)", f"{persecution_percentage:.1f}%")

# Show persecution links
st.subheader("🔗 Persecution Stories")
for _, row in persecution_df.tail(5).iterrows():
    st.markdown(f"[{row['month']} Persecution Report]({row['link']})")

# ===============================
# TESTIMONY LISTING
# ===============================
st.subheader("📝 Testimonies")

for index, row in filtered_df.iterrows():
    with st.expander(f"{row['category']} | {row['platform']} | Credibility: {row['credibility']}%"):
        st.write(f"**Age Range:** {row['age_range']}")
        st.write(f"**Believer:** {'Yes' if row['is_believer'] else 'No'}")
        st.write(f"**Description:** {row['description']}")
        st.markdown(f"[🔗 View Testimony]({row['link']})")

# ===============================
# AUTO REFRESH (every 30 mins)
# ===============================
st.caption("Data auto-refreshes every 30 minutes with simulated new testimonies.")
if st.button("🔄 Refresh Now"):
    df = generate_testimonies(300)
    persecution_df = generate_persecution_data(10)
    st.experimental_rerun()
