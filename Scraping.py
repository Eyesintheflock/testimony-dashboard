import requests
import praw
import json
from bs4 import BeautifulSoup

# ===========================
# YOUTUBE SCRAPING
# ===========================
def scrape_youtube_testimonies(api_key, max_results=10):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": "Christian testimony OR near death experience OR Jesus encounter",
        "type": "video",
        "maxResults": max_results,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    testimonies = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        title = item["snippet"]["title"]
        description = item["snippet"].get("description", "No description available.")
        channel_title = item["snippet"].get("channelTitle", "Unknown")

        # Fetch top comments
        comments_url = "https://www.googleapis.com/youtube/v3/commentThreads"
        comment_params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 5,
            "key": api_key
        }
        comment_response = requests.get(comments_url, params=comment_params)
        comments_data = comment_response.json()
        comments = [c["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    for c in comments_data.get("items", [])]

        testimonies.append({
            "platform": "YouTube",
            "title": title,
            "description": description,
            "source_url": video_url,
            "age_range": "Unknown",
            "credibility_score": 75,
            "is_believer": True,
            "comments": comments,
            "latitude": None,
            "longitude": None
        })

    return testimonies

# ===========================
# REDDIT SCRAPING
# ===========================
def scrape_reddit_testimonies(client_id, client_secret, user_agent, limit=10):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    testimonies = []
    for submission in reddit.subreddit("Christianity+TrueChristian+NearDeathExperiences").hot(limit=limit):
        comments = []
        submission.comments.replace_more(limit=0)
        for comment in submission.comments[:5]:
            comments.append(comment.body)

        testimonies.append({
            "platform": "Reddit",
            "title": submission.title,
            "description": submission.selftext[:300] + "..." if submission.selftext else "No description available.",
            "source_url": f"https://reddit.com{submission.permalink}",
            "age_range": "Unknown",
            "credibility_score": 70,
            "is_believer": True,
            "comments": comments,
            "latitude": None,
            "longitude": None
        })

    return testimonies

# ===========================
# TIKTOK SCRAPING (WORKAROUND)
# ===========================
def scrape_tiktok_testimonies():
    # TikTok API is private, so we simulate by searching via a public scraping endpoint or pre-built dataset.
    # In production, you'd integrate a TikTok scraper API.
    # For now, we return mock data to keep the dashboard functional.
    return [
        {
            "platform": "TikTok",
            "title": "Man shares powerful testimony of Jesus",
            "description": "A moving story of transformation.",
            "source_url": "https://www.tiktok.com/@example/video/123456789",
            "age_range": "25-34",
            "credibility_score": 85,
            "is_believer": True,
            "comments": ["This changed my life!", "Glory to God!", "Amen brother!"],
            "latitude": None,
            "longitude": None
        }
    ]

# ===========================
# PERSECUTION DATA SCRAPING
# ===========================
def scrape_persecution_data():
    url = "https://www.opendoors.org/en-US/persecution/countries/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    persecution_data = []

    # Example scraping for country persecution cases
    country_cards = soup.find_all("div", class_="country-card")
    for card in country_cards:
        country = card.find("h3").text.strip()
        link = card.find("a")["href"]

        persecution_data.append({
            "country": country,
            "latitude": None,  # You could add a mapping of country → coordinates if needed
            "longitude": None,
            "source_url": f"https://www.opendoors.org{link}"
        })

    return persecution_data
