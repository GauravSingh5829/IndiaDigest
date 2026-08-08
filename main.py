import argparse
from datetime import datetime
from scraping import scrape_google_news_rss, scrape_reddit_posts, scrape_youtube_comments
from sentiment import analyze_news_articles, analyze_reddit_posts, analyze_youtube_comments

DEFAULT_TOPICS = [
    "Lok Sabha Election",
    "ISRO Mission",
    "Indian Budget",
    "Bollywood",
    "Stock Market"
]

def run_pipeline(topics=None):
    if not topics:
        topics = DEFAULT_TOPICS

    print("=" * 60)
    print("IndiaDigest - Data Pipeline & Sentiment Engine")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    for topic in topics:
        print(f"\n Processing Topic: [{topic}]")
        print("-" * 40)
        
        # 1. Scrape Data
        news_file = scrape_google_news_rss(keyword=topic, max_articles=15)
        reddit_file = scrape_reddit_posts(keyword=topic, subreddit="india", limit=15)
        youtube_file = scrape_youtube_comments(topic=topic, max_videos=3, comments_per_video=15)

        # 2. Sentiment Analysis
        if news_file:
            analyze_news_articles(news_file)
        if reddit_file:
            analyze_reddit_posts(reddit_file)
        if youtube_file:
            analyze_youtube_comments(youtube_file)

    print("\n" + "=" * 60)
    print("[SUCCESS] Pipeline execution completed successfully!")
    print("Launch dashboard using: streamlit run streamlit_app.py")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IndiaDigest Scraping & Sentiment Pipeline")
    parser.add_argument("--topics", nargs="+", help="Topics to scrape (space-separated)", default=None)
    args = parser.parse_args()

    run_pipeline(topics=args.topics)
