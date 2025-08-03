import pandas as pd
import requests
from textblob import TextBlob
import praw
import os

# ======================
# YOUTUBE SCRAPING (REAL)
# ======================
def scrape_youtube_testimonies(query="Christian testimony"):
    api_key = os.getenv("YOUTUBE_API_KEY")
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=10&key={api_key}"
    response = requests.get(url).json()

    testimonies = []
    if "items" in response:
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            testimonies.append({
                "title": title,
                "platform": "YouTube",
                "age_range": "25-44",
                "credibility_score": 85,
                "description": description,
                "source_url": url,
                "is_believer": True,
                "latitude": 37.7749,
                "longitude": -122.4194
            })
    return testimonies

# ======================
# REDDIT SCRAPING (REAL)
# ======================
def scrape_reddit_testimonies(subreddit="Christianity"):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="testimony_scraper"
    )

    testimonies = []
    for post in reddit.subreddit(subreddit).hot(limit=10):
        testimonies.append({
            "title": post.title,
            "platform": "Reddit",
            "age_range": "18-34",
            "credibility_score": 80,
            "description": post.selftext[:250] if post.selftext else "Link Post",
            "source_url": f"https://reddit.com{post.permalink}",
            "is_believer": True,
            "latitude": 40.7128,
            "longitude": -74.0060
        })
    return testimonies

# ======================
# TIKTOK (PLACEHOLDER)
# ======================
def scrape_tiktok_testimonies():
    return [
        {
            "title": "Miracle Healing Story",
            "platform": "TikTok",
            "age_range": "25-34",
            "credibility_score": 95,
            "description": "A viral TikTok testimony of miraculous healing.",
            "source_url": "https://tiktok.com/example1",
            "is_believer": True,
            "latitude": 34.0522,
            "longitude": -118.2437
        }
    ]

# ======================
# SENTIMENT ANALYSIS
# ======================
def analyze_comment_sentiment(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0.1:
        return "Positive"
    elif analysis.sentiment.polarity < -0.1:
        return "Negative"
    return "Neutral"

# ======================
# PERSECUTION DATA LOADER
# ======================
def scrape_persecution_data_from_csv():
    return pd.read_csv("persecution_data.csv").to_dict(orient="records")
