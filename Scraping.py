import requests
from bs4 import BeautifulSoup
import re

# ======================
# PROPHECY KEYWORDS
# ======================
PROPHECY_KEYWORDS = {
    "Rapture": ["rapture", "caught up", "taken up"],
    "Second Coming": ["second coming", "Jesus return", "Christ's return"],
    "End Times": ["end times", "tribulation", "apocalypse", "mark of the beast"],
    "Visions & Dreams": ["vision", "dream", "prophetic word"],
}

def detect_prophecy_category(text):
    text = text.lower()
    matched_categories = []
    for category, keywords in PROPHECY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)
    return matched_categories if matched_categories else ["General"]

# ======================
# SCRAPE YOUTUBE
# ======================
def scrape_youtube_testimonies():
    data = []
    # Simulated API or scraping logic
    testimonies = [
        {
            "title": "I Saw Jesus in a Vision",
            "description": "A dream of the rapture and second coming of Jesus that changed my life.",
            "platform": "YouTube",
            "is_believer": True,
            "credibility_score": 87,
            "age_range": "25-34",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "source_url": "https://www.youtube.com/watch?v=example"
        },
        {
            "title": "Former Atheist Shares His Testimony",
            "description": "I used to mock God, but after a near-death experience, I now believe.",
            "platform": "YouTube",
            "is_believer": False,
            "credibility_score": 78,
            "age_range": "35-44",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "source_url": "https://www.youtube.com/watch?v=example2"
        }
    ]

    for t in testimonies:
        t["prophecy_categories"] = detect_prophecy_category(t["description"])
        data.append(t)
    return data

# ======================
# SCRAPE REDDIT
# ======================
def scrape_reddit_testimonies():
    data = []
    testimonies = [
        {
            "title": "End Times Dream",
            "description": "I had a dream of the apocalypse, and I believe it was prophetic.",
            "platform": "Reddit",
            "is_believer": True,
            "credibility_score": 83,
            "age_range": "18-24",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "source_url": "https://www.reddit.com/r/Christianity/example"
        }
    ]
    for t in testimonies:
        t["prophecy_categories"] = detect_prophecy_category(t["description"])
        data.append(t)
    return data

# ======================
# SCRAPE TIKTOK
# ======================
def scrape_tiktok_testimonies():
    data = []
    testimonies = [
        {
            "title": "Prophetic Word About the Rapture",
            "description": "This message was revealed in a vision. The rapture is near.",
            "platform": "TikTok",
            "is_believer": True,
            "credibility_score": 90,
            "age_range": "18-24",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "source_url": "https://www.tiktok.com/@example/video/12345"
        }
    ]
    for t in testimonies:
        t["prophecy_categories"] = detect_prophecy_category(t["description"])
        data.append(t)
    return data

# ======================
# SCRAPE PERSECUTION DATA
# ======================
def scrape_persecution_data():
    # In a real scenario, you'd pull this from an API or a global watchlist
    return [
        {"country": "Nigeria", "cases": 4300},
        {"country": "China", "cases": 2100},
        {"country": "India", "cases": 1700},
        {"country": "Pakistan", "cases": 1500},
        {"country": "North Korea", "cases": 2800},
        {"country": "United States", "cases": 120},
        {"country": "United Kingdom", "cases": 90}
    ]
