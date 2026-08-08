import os
import praw
import pandas as pd
from datetime import datetime
from config import REDDIT, DATA_DIR

def get_reddit_client():
    if not REDDIT["client_id"] or not REDDIT["client_secret"]:
        print("[!] Warning: Reddit API credentials not configured in environment or .env file.")
        return None

    try:
        reddit = praw.Reddit(
            client_id=REDDIT["client_id"],
            client_secret=REDDIT["client_secret"],
            user_agent=REDDIT["user_agent"],
            username=REDDIT["username"] if REDDIT["username"] else None,
            password=REDDIT["password"] if REDDIT["password"] else None
        )
        return reddit
    except Exception as e:
        print(f"[!] Failed to initialize Reddit client: {e}")
        return None

def scrape_reddit_posts(keyword="India", subreddit="india", limit=20):
    """
    Scrape top posts from Reddit matching a keyword.
    """
    print(f"[*] Scraping Reddit (r/{subreddit}) for keyword: '{keyword}'...")
    reddit = get_reddit_client()
    posts = []

    if reddit:
        try:
            for post in reddit.subreddit(subreddit).search(keyword, sort="top", limit=limit):
                posts.append({
                    "id": post.id,
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "num_comments": post.num_comments,
                    "created": datetime.fromtimestamp(post.created),
                    "subreddit": subreddit
                })
        except Exception as e:
            print(f"[!] Reddit API fetch error: {e}")

    df = pd.DataFrame(posts)
    if df.empty:
        df = pd.DataFrame(columns=["id", "title", "score", "url", "num_comments", "created", "subreddit"])

    filename = f"reddit_{keyword.replace(' ', '_')}_{datetime.today().date()}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"[+] Saved {len(df)} Reddit posts for '{keyword}' -> {filepath}")
    return filepath
