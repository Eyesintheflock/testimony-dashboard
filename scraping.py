import os
import pandas as pd
from googleapiclient.discovery import build
import requests

# Load API key from environment variable
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("Missing YouTube API key. Please set it in your Streamlit secrets or environment variables.")

# YouTube API setup
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def scrape_youtube_testimonies(query="Christian testimony", max_results=10):
    results = []
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"].get("description", "")
        channel_title = item["snippet"]["channelTitle"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        results.append({
            "platform": "YouTube",
            "title": title,
            "description": description,
            "source_url": video_url,
            "age_range": "Unknown",
            "credibility_score": 0,
            "is_believer": True,
            "author": channel_title
        })

    return pd.DataFrame(results)

def scrape_reddit_testimonies(subreddit="Christianity", query="testimony", limit=10):
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&sort=new"
    headers = {"User-agent": "testimony-dashboard"}
    response = requests.get(url, headers=headers)
    results = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", {}).get("children", []):
            post = item["data"]
            results.append({
                "platform": "Reddit",
                "title": post.get("title", "No title"),
                "description": post.get("selftext", ""),
                "source_url": f"https://www.reddit.com{post.get('permalink', '')}",
                "age_range": "Unknown",
                "credibility_score": 0,
                "is_believer": True,
                "author": post.get("author", "Unknown")
            })
    return pd.DataFrame(results)

def scrape_tiktok_testimonies():
    # Placeholder: TikTok requires third-party APIs or scraping libraries
    return pd.DataFrame([])

def scrape_persecution_data():
    return pd.read_csv("persecution_data.csv")
