import streamlit as st
from googleapiclient.discovery import build

# Load YouTube API key securely from Streamlit secrets
YOUTUBE_API_KEY = st.secrets["api_keys"]["youtube"]

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def scrape_youtube_testimonies(query="Christian testimony"):
    youtube = get_youtube_client()
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=10,
        type="video",
        order="date"
    )
    response = request.execute()

    data = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        channel = item["snippet"]["channelTitle"]
        published_at = item["snippet"]["publishedAt"]

        data.append({
            "title": title,
            "description": description,
            "platform": "YouTube",
            "source_url": video_url,
            "channel": channel,
            "published_at": published_at,
            "is_believer": None,
            "credibility_score": None,
            "age_range": "Unknown"
        })
    return data
