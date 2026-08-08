import os
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, DATA_DIR

def get_youtube_service():
    if not YOUTUBE_API_KEY:
        print("[!] Warning: YOUTUBE_API_KEY not configured in environment or .env file.")
        return None
    try:
        return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        print(f"[!] Failed to build YouTube service: {e}")
        return None

def search_videos(service, query, max_results=5):
    try:
        request = service.search().list(
            part='snippet',
            q=query,
            maxResults=max_results,
            type='video',
            relevanceLanguage='en',
            regionCode='IN'
        )
        response = request.execute()
        video_ids = []
        for item in response.get('items', []):
            if 'videoId' in item.get('id', {}):
                video_ids.append(item['id']['videoId'])
        return video_ids
    except Exception as e:
        print(f"[!] YouTube Search error: {e}")
        return []

def fetch_comments(service, video_id, max_comments=20):
    comments = []
    try:
        request = service.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(max_comments, 100),
            textFormat='plainText'
        )
        response = request.execute()
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                "video_id": video_id,
                "author": comment['authorDisplayName'],
                "comment": comment['textDisplay'],
                "published_at": comment['publishedAt'],
                "like_count": comment['likeCount']
            })
    except Exception as e:
        print(f"[!] Skipped YouTube video {video_id} - {e}")
    return comments

def scrape_youtube_comments(topic="India", max_videos=3, comments_per_video=20):
    print(f"[*] Scraping YouTube comments for topic: '{topic}'...")
    service = get_youtube_service()
    all_comments = []

    if service:
        video_ids = search_videos(service, topic, max_results=max_videos)
        for vid in video_ids:
            video_comments = fetch_comments(service, vid, max_comments=comments_per_video)
            all_comments.extend(video_comments)

    df = pd.DataFrame(all_comments)
    if df.empty:
        df = pd.DataFrame(columns=["video_id", "author", "comment", "published_at", "like_count"])

    filename = f"youtube_{topic.replace(' ', '_')}_{datetime.today().date()}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"[+] Saved {len(df)} YouTube comments for '{topic}' -> {filepath}")
    return filepath
