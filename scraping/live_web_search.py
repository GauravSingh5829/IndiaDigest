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

def perform_live_web_search(query, max_results=12):
    clean_q = normalize_query(query)
    results = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 1. Google News RSS Search
    try:
        encoded_q = urllib.parse.quote(clean_q)
        feed_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(feed_url)
        
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
                    "summary": summary if summary else title,
                    "link": link,
                    "published": pub_date,
                    "source": "News",
                    "query": clean_q
                })
    except Exception as e:
        print(f"[!] News search note: {e}")

    # 2. DuckDuckGo Search API / HTML (if Google RSS yields < 3 items)
    if len(results) < 3:
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
                            "summary": title,
                            "link": link,
                            "published": "Recent",
                            "source": "Web",
                            "query": clean_q
                        })
        except Exception as e:
            print(f"[!] Web search note: {e}")

    return results, clean_q
