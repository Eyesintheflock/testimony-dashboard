import pandas as pd
import requests
from textblob import TextBlob
import praw
import os

# ======================
# CREDIBILITY SCORING
# ======================
def calculate_credibility_score(posting_frequency, sentiment_score, ridicule_factor, platform):
    platform_weights = {
        "YouTube": 1.0,
        "Reddit": 0.9,
        "TikTok": 0.8,
        "Instagram": 0.85,
        "X": 0.88
    }
    platform_weight = platform_weights.get(platform, 0.85)

    # Formula:
    credibility = (0.4 * posting_frequency) + (0.3 * sentiment_score) + (0.2 * ridicule_factor) + (0.1 * platform_weight)
    return min(100, max(0, round(credibility * 100)))

# ======================
# SENTIMENT ANALYSIS
# ======================
def analyze_comment_sentiment(comment):
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0.1:
        return 1.0  # Positive
    elif analysis.sentiment.polarity < -0.1:
        return 0.7  # Ridicule increases credibility slightly
    return 0.85  # Neutral comments give mid credibility

# ======================
# MOCK COMMENT SCRAPER
# ======================
def fetch_comments_sentiment(testimony_url):
    # In production: scrape YouTube or Reddit comments
    # Placeholder: simulate sentiment mix
    comments = [
        "This is amazing!", 
        "I don’t believe this.", 
        "God is real!", 
        "Fake story.", 
        "Praise Jesus!"
    ]
    sentiments = [analyze_comment_sentiment(c) for c in comments]
    return sum(sentiments) / len(sentiments)

# ======================
# YOUTUBE SCRAPING
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

            # Calculate credibility dynamically
            sentiment_score = fetch_comments_sentiment(url)
            ridicule_factor = 1.2 if sentiment_score < 0.8 else 1.0
            posting_frequency = 0.9  # placeholder, could be API-driven

            credibility = calculate_credibility_score(posting_frequency, sentiment_score, ridicule_factor, "YouTube")

            testimonies.append({
                "title": title,
                "platform": "YouTube",
                "age_range": "25-44",
                "credibility_score": credibility,
                "description": description,
                "source_url": url,
                "is_believer": True,
                "latitude": 37.7749,
                "longitude": -122.4194
            })
    return testimonies

# ======================
# REDDIT SCRAPING
# ======================
def scrape_reddit_testimonies(subreddit="Christianity"):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="testimony_scraper"
    )

    testimonies = []
    for post in reddit.subreddit(subreddit).hot(limit=10):
        sentiment_score = fetch_comments_sentiment(f"https://reddit.com{post.permalink}")
        ridicule_factor = 1.2 if sentiment_score < 0.8 else 1.0
        posting_frequency = 0.85  # simulated

        credibility = calculate_credibility_score(posting_frequency, sentiment_score, ridicule_factor, "Reddit")

        testimonies.append({
            "title": post.title,
            "platform": "Reddit",
            "age_range": "18-34",
            "credibility_score": credibility,
            "description": post.selftext[:250] if post.selftext else "Link Post",
            "source_url": f"https://reddit.com{post.permalink}",
            "is_believer": True,
            "latitude": 40.7128,
            "longitude": -74.0060
        })
    return testimonies

# ======================
# TIKTOK SCRAPING
# ======================
def scrape_tiktok_testimonies():
    sentiment_score = 0.9
    ridicule_factor = 1.0
    posting_frequency = 0.8

    credibility = calculate_credibility_score(posting_frequency, sentiment_score, ridicule_factor, "TikTok")

    return [
        {
            "title": "Miracle Healing Story",
            "platform": "TikTok",
            "age_range": "25-34",
            "credibility_score": credibility,
            "description": "A viral TikTok testimony of miraculous healing.",
            "source_url": "https://tiktok.com/example1",
            "is_believer": True,
            "latitude": 34.0522,
            "longitude": -118.2437
        }
    ]

# ======================
# PERSECUTION DATA (REAL TIME SCRAPING)
# ======================
def scrape_persecution_data():
    url = "https://raw.githubusercontent.com/owid/persecution-data/main/persecution.csv"
    try:
        df = pd.read_csv(url)
        return df.to_dict(orient="records")
    except:
        return pd.read_csv("persecution_data.csv").to_dict(orient="records")
