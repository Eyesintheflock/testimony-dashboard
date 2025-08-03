# Testimony Dashboard

An interactive real-time dashboard for viewing, analyzing, and exploring Christian testimonies, near-death experiences, and persecution data from around the world.

## Features
- 🕒 Real-time scraping of testimony data every 30 minutes
- 🌍 Interactive global map of testimonies by region
- 📊 Credibility scoring based on user engagement and behavior
- ✝️ Comparison between testimonies from believers vs. non-believers
- 🔗 Clickable links to the original source of each testimony (YouTube, Reddit, blogs, etc.)
- 📈 Visual charts for:
  - Testimonies per platform
  - Persecution data by country
  - Believer vs. non-believer testimonies
- 🔍 Short descriptions for each testimony with previews
- 🔄 Automated data updates with no manual refresh needed

## Files
- `dashboard.py` – Main Streamlit app.
- `scraping.py` – Real-time scraping logic for testimonies and comments.
- `testimonies.csv` – Stores testimony data.
- `persecution_data.csv` – Global persecution statistics.
- `requirements.txt` – Python dependencies for Streamlit deployment.

## How to Run Locally
```bash
# Clone the repository
git clone https://github.com/Eyesintheflock/testimony-dashboard.git
cd testimony-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run dashboard.py
