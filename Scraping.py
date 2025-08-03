import os
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# ===========================
# YOUTUBE SCRAPER
# ===========================

def scrape_youtube_testimonies(api_key, query="Christian testimony", max_results=5):
    youtube = build("youtube", "v3", developerKey=api_key)
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    testimonies = []

    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        channel = item["snippet"]["channelTitle"]

        comments = scrape_youtube_comments(api_key, video_id)
        credibility_score = calculate_credibility_score(description, comments)

        testimonies.append({
            "title": title,
            "platform": "YouTube",
            "source_url": f"https://www.youtube.com/watch?v={video_id}",
            "description": description,
            "age_range": estimate_age_range(description),
            "credibility_score": credibility_score,
            "is_believer": detect_believer(description),
            "comments": comments
        })

    return testimonies


def scrape_youtube_comments(api_key, video_id, max_comments=20):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_comments,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments


# ===========================
# REDDIT SCRAPER
# ===========================

def scrape_reddit_testimonies(client_id, client_secret, user_agent, subreddit="Christianity", limit=5):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    testimonies = []

    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        comments = scrape_reddit_comments(submission)
        credibility_score = calculate_credibility_score(submission.title, comments)

        testimonies.append({
            "title": submission.title,
            "platform": "Reddit",
            "source_url": submission.url,
            "description": submission.selftext[:300] + "...",
            "age_range": "Unknown",
            "credibility_score": credibility_score,
            "is_believer": detect_believer(submission.title),
            "comments": comments
        })

    return testimonies


def scrape_reddit_comments(submission, max_comments=20):
    submission.comments.replace_more(limit=0)
    comments = []
    for comment in submission.comments[:max_comments]:
        comments.append(comment.body)
    return comments


# ===========================
# TIKTOK SCRAPER (Placeholder)
# ===========================

def scrape_tiktok_testimonies():
    # TikTok scraping requires an unofficial API or external service.
    return [
        {
            "title": "TikTok Testimony Example",
            "platform": "TikTok",
            "source_url": "https://www.tiktok.com/example",
            "description": "Placeholder TikTok testimony",
            "age_range": "18-25",
            "credibility_score": 75,
            "is_believer": True,
            "comments": ["Amazing!", "This blessed me!", "Praise God!"]
        }
    ]


# ===========================
# HELPER FUNCTIONS
# ===========================

def calculate_credibility_score(description, comments):
    sentiment_scores = [sia.polarity_scores(c)["compound"] for c in comments]
    avg_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0

    positive_comments = sum(1 for s in sentiment_scores if s > 0.2)
    negative_comments = sum(1 for s in sentiment_scores if s < -0.2)

    ridicule_factor = (negative_comments / max(len(sentiment_scores), 1)) * 50
    support_factor = (positive_comments / max(len(sentiment_scores), 1)) * 50

    frequency_factor = 10 if "testimony" in description.lower() or "rapture" in description.lower() else 0

    credibility_score = 50 + support_factor - ridicule_factor + frequency_factor
    return max(0, min(100, credibility_score))


def detect_believer(description):
    keywords = ["Jesus", "God", "testimony", "faith", "salvation"]
    return any(word.lower() in description.lower() for word in keywords)


def estimate_age_range(description):
    if "teen" in description.lower():
        return "13-19"
    elif "youth" in description.lower() or "college" in description.lower():
        return "18-25"
    elif "father" in description.lower() or "mother" in description.lower():
        return "30-50"
    else:
        return "Unknown"
