import requests
import os
import pandas as pd
import praw
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import time

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER_AGENT = "testimony_dashboard"
TIKTOK_SCRAPER_URL = "https://api.tiktok-scraper.com"  # Example placeholder, replace with actual scraper API

# ======================
# YOUTUBE SCRAPER (REAL)
# ======================
def scrape_youtube_testimonies(query="Christian testimony"):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=10,
        type="video"
    )
    response = request.execute()

    testimonies = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        # Sentiment score based on comments
        credibility_score = analyze_youtube_comments(video_id)

        testimonies.append({
            "title": title,
            "platform": "YouTube",
            "is_believer": detect_believer(description),
            "age_range": estimate_age_from_text(description),
            "credibility_score": credibility_score,
            "description": description,
            "prophecy_categories": detect_prophecy_category(description),
            "source_url": url,
            "longitude": None,
            "latitude": None,
        })
    return testimonies

def analyze_youtube_comments(video_id):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=20
    )
    response = request.execute()

    sentiment_scores = []
    for item in response.get("items", []):
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        sentiment = TextBlob(comment_text).sentiment.polarity
        sentiment_scores.append(sentiment)
    return int(((sum(sentiment_scores) / len(sentiment_scores)) + 1) * 50) if sentiment_scores else 50

# ======================
# REDDIT SCRAPER (REAL)
# ======================
def scrape_reddit_testimonies(subreddit="Christianity"):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

    testimonies = []
    for submission in reddit.subreddit(subreddit).search("testimony", limit=10):
        credibility_score = analyze_reddit_comments(submission)

        testimonies.append({
            "title": submission.title,
            "platform": "Reddit",
            "is_believer": detect_believer(submission.selftext),
            "age_range": estimate_age_from_text(submission.selftext),
            "credibility_score": credibility_score,
            "description": submission.selftext[:200] + "...",
            "prophecy_categories": detect_prophecy_category(submission.selftext),
            "source_url": submission.url,
            "longitude": None,
            "latitude": None,
        })
    return testimonies

def analyze_reddit_comments(submission):
    submission.comments.replace_more(limit=0)
    sentiment_scores = []
    for comment in submission.comments.list():
        sentiment = TextBlob(comment.body).sentiment.polarity
        sentiment_scores.append(sentiment)
    return int(((sum(sentiment_scores) / len(sentiment_scores)) + 1) * 50) if sentiment_scores else 50

# ======================
# TIKTOK SCRAPER (REAL)
# ======================
def scrape_tiktok_testimonies():
    response = requests.get(f"{TIKTOK_SCRAPER_URL}/search?query=Christian testimony")
    data = response.json()

    testimonies = []
    for item in data.get("results", []):
        testimonies.append({
            "title": item["title"],
            "platform": "TikTok",
            "is_believer": detect_believer(item["description"]),
            "age_range": estimate_age_from_text(item["description"]),
            "credibility_score": 85,  # Placeholder until comment scraping added
            "description": item["description"],
            "prophecy_categories": detect_prophecy_category(item["description"]),
            "source_url": item["url"],
            "longitude": None,
            "latitude": None,
        })
    return testimonies

# ======================
# PERSECUTION DATA SCRAPER (REAL)
# ======================
def scrape_persecution_data():
    url = "https://www.opendoors.org/en-US/persecution/countries/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    country_elements = soup.select(".country-list-item")
    for country in country_elements:
        name = country.select_one(".country-name").text.strip()
        cases = int(re.sub(r"\D", "", country.select_one(".persecution-cases").text))
        link = country.find("a", href=True)["href"]

        data.append({
            "country": name,
            "cases": cases,
            "source_url": f"https://www.opendoors.org{link}"
        })
    return data

# ======================
# HELPERS
# ======================
def detect_believer(text):
    return bool(re.search(r"\bJesus\b|\bGod\b|\bBible\b|\bChristian\b", text, re.IGNORECASE))

def detect_prophecy_category(text):
    categories = []
    if re.search(r"\brapture\b", text, re.IGNORECASE):
        categories.append("Rapture")
    if re.search(r"\bsecond coming\b", text, re.IGNORECASE):
        categories.append("Second Coming")
    if re.search(r"\bvision\b|\bdream\b", text, re.IGNORECASE):
        categories.append("Visions")
    return categories if categories else ["General"]

def estimate_age_from_text(text):
    if "teen" in text.lower():
        return "13-19"
    elif "college" in text.lower() or "20" in text:
        return "20-29"
    elif "30" in text:
        return "30-39"
    else:
        return "Unknown"
