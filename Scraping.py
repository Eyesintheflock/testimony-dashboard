import pandas as pd
from googleapiclient.discovery import build
import random

# ================================
# Helper: Credibility Scoring
# ================================
def calculate_credibility(comment_sentiment, testimony_ratio):
    """
    Calculate credibility score:
    - Sentiment: Positive vs negative comments.
    - Testimony ratio: % of creator content that is testimony-related.
    """
    base_score = 50

    # Sentiment weighting
    sentiment_boost = (comment_sentiment * 30)  # up to +30 for very positive sentiment
    testimony_boost = (testimony_ratio * 20)    # up to +20 for mostly testimony content

    credibility_score = base_score + sentiment_boost + testimony_boost
    return min(max(int(credibility_score), 0), 100)  # clamp between 0–100


# ================================
# YouTube Scraper (Real)
# ================================
def scrape_youtube_testimonies(api_key, search_query="Christian testimony"):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        q=search_query,
        part="snippet",
        maxResults=10,
        type="video",
        order="date"
    )
    response = request.execute()

    results = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        channel_id = item["snippet"]["channelId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Analyze comments sentiment
        sentiment_score = analyze_youtube_comments(youtube, video_id)

        # Check creator posting behavior
        testimony_ratio = analyze_channel_behavior(youtube, channel_id)

        credibility_score = calculate_credibility(sentiment_score, testimony_ratio)

        results.append({
            "title": title,
            "platform": "YouTube",
            "age_range": "Unknown",  # Placeholder until NLP on description for age detection
            "credibility_score": credibility_score,
            "description": description,
            "is_believer": credibility_score > 60,
            "source_url": video_url,
            "latitude": 37.7749,
            "longitude": -122.4194
        })

    return results


# ================================
# Analyze YouTube Comments
# ================================
def analyze_youtube_comments(youtube, video_id):
    """Return sentiment score from 0–1 based on comments."""
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            textFormat="plainText"
        )
        response = request.execute()

        positive, negative = 0, 0
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"].lower()
            if any(word in comment for word in ["amazing", "praise", "thank", "blessed"]):
                positive += 1
            elif any(word in comment for word in ["fake", "liar", "clout", "scam"]):
                negative += 1

        total = positive + negative
        return positive / total if total > 0 else 0.5  # neutral baseline

    except:
        return 0.5  # default neutral if API fails


# ================================
# Analyze Creator Channel Behavior
# ================================
def analyze_channel_behavior(youtube, channel_id):
    """Check how much of a creator's content is testimony-related."""
    try:
        request = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            maxResults=10,
            order="date"
        )
        response = request.execute()

        testimony_videos = 0
        for item in response.get("items", []):
            title = item["snippet"]["title"].lower()
            if any(keyword in title for keyword in ["testimony", "jesus", "vision", "rapture"]):
                testimony_videos += 1

        return testimony_videos / 10  # 0–1 ratio
    except:
        return 0.5  # assume balanced if API fails


# ================================
# TikTok Scraper (Placeholder)
# ================================
def scrape_tiktok_testimonies():
    return [
        {
            "title": "TikTok Testimony Example",
            "platform": "TikTok",
            "age_range": "18-24",
            "credibility_score": 75,
            "description": "A short video testimony on TikTok.",
            "is_believer": True,
            "source_url": "https://tiktok.com/example-testimony",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    ]


# ================================
# Reddit Scraper (Placeholder)
# ================================
def scrape_reddit_testimonies():
    return [
        {
            "title": "Reddit Testimony Example",
            "platform": "Reddit",
            "age_range": "35-44",
            "credibility_score": 88,
            "description": "Detailed testimony shared in r/Christianity.",
            "is_believer": True,
            "source_url": "https://reddit.com/example-testimony",
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    ]


# ================================
# Combine All Sources
# ================================
def scrape_all_sources(api_key=None):
    youtube_data = scrape_youtube_testimonies(api_key) if api_key else []
    tiktok_data = scrape_tiktok_testimonies()
    reddit_data = scrape_reddit_testimonies()

    all_data = youtube_data + tiktok_data + reddit_data
    return pd.DataFrame(all_data)
