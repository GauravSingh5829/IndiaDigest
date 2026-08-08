import os
import pandas as pd
from .analyzer import get_sentiment

def analyze_news_articles(file_path):
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return None

    df = pd.read_csv(file_path)
    if df.empty:
        print(f"[!] Empty news file: {file_path}")
        return file_path

    if 'title' in df.columns:
        df['title_sentiment'] = df['title'].astype(str).apply(get_sentiment)
    if 'summary' in df.columns:
        df['summary_sentiment'] = df['summary'].astype(str).apply(get_sentiment)

    output_path = file_path.replace(".csv", "_sentiment.csv") if not file_path.endswith("_sentiment.csv") else file_path
    df.to_csv(output_path, index=False)
    print(f"[+] News sentiment analyzed -> {output_path}")
    return output_path
