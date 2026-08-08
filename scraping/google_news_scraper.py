import os
import feedparser
import pandas as pd
from urllib.parse import quote
from datetime import datetime
from config import DATA_DIR

def scrape_google_news_rss(keyword="India", max_articles=15):
    """
    Scrape news articles from Google News RSS based on a keyword.
    """
    encoded_keyword = quote(keyword)
    print(f"[*] Scraping Google News RSS for keyword: '{keyword}'...")
    feed_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in getattr(feed, 'entries', [])[:max_articles]:
        articles.append({
            "title": getattr(entry, 'title', ''),
            "link": getattr(entry, 'link', ''),
            "published": getattr(entry, 'published', ''),
            "summary": getattr(entry, 'summary', '')
        })

    df = pd.DataFrame(articles)
    if df.empty:
        df = pd.DataFrame(columns=["title", "link", "published", "summary"])

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"news_{keyword.replace(' ', '_')}_{today}.csv"
    filepath = os.path.join(DATA_DIR, filename)

    df.to_csv(filepath, index=False)
    print(f"[+] Scraped {len(df)} articles on '{keyword}' -> {filepath}")
    return filepath
