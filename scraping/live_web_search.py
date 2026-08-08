import re
import urllib.parse
import requests
import feedparser
from bs4 import BeautifulSoup

QUERY_CORRECTIONS = {
    "platnium": "platinum",
    "goldprice": "gold price",
    "electon": "election",
    "budg": "budget",
    "stockmarket": "stock market"
}

def normalize_query(query):
    query_clean = query.strip()
    words = query_clean.split()
    corrected_words = [QUERY_CORRECTIONS.get(w.lower(), w) for w in words]
    return " ".join(corrected_words)

def perform_live_web_search(query, max_results=10):
    clean_q = normalize_query(query)
    results = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    # 1. Google News RSS Search via requests
    try:
        encoded_q = urllib.parse.quote(clean_q)
        feed_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-IN&gl=IN&ceid=IN:en"
        resp = requests.get(feed_url, headers=headers, timeout=6)
        if resp.status_code == 200:
            feed = feedparser.parse(resp.content)
            for entry in getattr(feed, 'entries', [])[:max_results]:
                title = getattr(entry, 'title', '').strip()
                summary = getattr(entry, 'summary', '').strip()
                link = getattr(entry, 'link', '')
                pub_date = getattr(entry, 'published', '')

                if summary:
                    try:
                        summary = BeautifulSoup(summary, "html.parser").get_text()
                    except Exception:
                        pass

                if title:
                    results.append({
                        "title": title,
                        "text": title,
                        "summary": summary if summary else title,
                        "link": link,
                        "published": pub_date,
                        "date": pub_date,
                        "source": "News",
                        "topic": clean_q.title(),
                        "query": clean_q
                    })
    except Exception as e:
        print(f"[!] News search note: {e}")

    # 2. DuckDuckGo HTML (if Google RSS yields < 2 items)
    if len(results) < 2:
        try:
            ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(clean_q + ' news India')}"
            resp = requests.get(ddg_url, headers=headers, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for a in soup.find_all('a', class_='result__a', limit=max_results):
                    title = a.get_text().strip()
                    link = a.get('href', '')
                    if title and len(title) > 10:
                        results.append({
                            "title": title,
                            "text": title,
                            "summary": title,
                            "link": link,
                            "published": "Recent",
                            "date": "Recent",
                            "source": "Web",
                            "topic": clean_q.title(),
                            "query": clean_q
                        })
        except Exception as e:
            print(f"[!] Web search note: {e}")

    return results, clean_q
