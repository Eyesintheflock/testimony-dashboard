import requests
import praw
import json
from bs4 import BeautifulSoup

# ===========================
# GEOLOCATION HELPER
# ===========================
def get_coordinates(location_name, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {"q": location_name, "key": api_key, "limit": 1}
    response = requests.get(url, params=params).json()

    if response["results"]:
        lat = response["results"][0]["geometry"]["lat"]
        lng = response["results"][0]["geometry"]["lng"]
        return lat, lng
    return None, None

# ===========================
# YOUTUBE SCRAPING
# ===========================
def scrape_youtube_testimonies(api_key, geocode_key, max_results=10):
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

        # Estimate location based on channel title (if applicable)
        lat, lng = get_coordinates(channel_title, geocode_key)

        testimonies.append({
            "platform": "YouTube",
            "title": title,
            "description": description,
            "source_url": video_url,
            "age_range": "Unknown",
            "credibility_score": 75,
            "is_believer": True,
            "comments": comments,
            "latitude": lat,
            "longitude": lng
        })

    return testimonies

# ===========================
# REDDIT SCRAPING
# ===========================
def scrape_reddit_testimonies(client_id, client_secret, user_agent, geocode_key, limit=10):
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

        # Attempt to geocode based on subreddit context or default "United States"
        lat, lng = get_coordinates("United States", geocode_key)

        testimonies.append({
            "platform": "Reddit",
            "title": submission.title,
            "description": submission.selftext[:300] + "..." if submission.selftext else "No description available.",
            "source_url": f"https://reddit.com{submission.permalink}",
            "age_range": "Unknown",
            "credibility_score": 70,
            "is_believer": True,
            "comments": comments,
            "latitude": lat,
            "longitude": lng
        })

    return testimonies

# ===========================
# TIKTOK SCRAPING (WORKAROUND)
# ===========================
def scrape_tiktok_testimonies(geocode_key):
    # Placeholder TikTok testimony data
    lat, lng = get_coordinates("Texas, USA", geocode_key)
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
            "latitude": lat,
            "longitude": lng
        }
    ]

# ===========================
# PERSECUTION DATA SCRAPING
# ===========================
def scrape_persecution_data(geocode_key):
    url = "https://www.opendoors.org/en-US/persecution/countries/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    persecution_data = []

    country_cards = soup.find_all("div", class_="country-card")
    for card in country_cards:
        country = card.find("h3").text.strip()
        link = card.find("a")["href"]

        lat, lng = get_coordinates(country, geocode_key)

        persecution_data.append({
            "country": country,
            "latitude": lat,
            "longitude": lng,
            "source_url": f"https://www.opendoors.org{link}"
        })

    return persecution_data
