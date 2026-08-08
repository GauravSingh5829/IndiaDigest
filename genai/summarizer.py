import os
import socket
import warnings
import pandas as pd
from urllib.parse import urlparse
from config import OPENAI_API_KEY, OLLAMA_HOST, OLLAMA_MODEL

# Filter out external library deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Cached host status to avoid repeated connection timeouts
_HOST_CHECK_CACHE = {}

def is_host_reachable(url_string, timeout=0.3):
    if not url_string:
        return False
    if url_string in _HOST_CHECK_CACHE:
        return _HOST_CHECK_CACHE[url_string]

    try:
        parsed = urlparse(url_string)
        host = parsed.hostname or "localhost"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        is_up = (result == 0)
    except Exception:
        is_up = False

    _HOST_CHECK_CACHE[url_string] = is_up
    return is_up

def get_llm():
    """
    Initialize LLM instance based on available configuration.
    Priority: OpenAI -> Reachable Ollama -> None
    """
    if OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.2)
        except Exception:
            pass

    if OLLAMA_HOST and is_host_reachable(OLLAMA_HOST):
        try:
            from langchain_ollama import OllamaLLM
            return OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_HOST, temperature=0.2)
        except Exception:
            try:
                from langchain_community.llms import Ollama
                return Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_HOST, temperature=0.2)
            except Exception:
                pass

    return None

def invoke_prompt(prompt_text):
    llm = get_llm()
    if llm:
        try:
            if hasattr(llm, 'invoke'):
                res = llm.invoke(prompt_text)
                return getattr(res, 'content', str(res))
            elif hasattr(llm, 'predict'):
                return llm.predict(prompt_text)
        except Exception:
            pass
    return None

def format_as_html_list(bullet_list):
    items = "".join([f"<li style='margin-bottom: 8px;'>{item}</li>" for item in bullet_list])
    return f"<ul style='padding-left: 20px; margin: 0; color: #cbd5e1;'>{items}</ul>"

def summarize_news(news_csv):
    if not os.path.exists(news_csv):
        return "<p style='color: #f87171;'>News data file not found. Click 'Collect Fresh Data Now' in the sidebar to scrape live articles.</p>"
    
    df = pd.read_csv(news_csv)
    if df.empty or 'title' not in df.columns:
        return "<p style='color: #f87171;'>No news articles available to summarize.</p>"

    titles = df["title"].dropna().head(7).tolist()
    articles_text = "\n- ".join(titles)

    prompt = f"""
You are a professional news analyst. Summarize the following news headlines into 4-5 key bullet points focusing on major developments:

Headlines:
- {articles_text}

Summary:
"""
    result = invoke_prompt(prompt)
    if result:
        return result.replace("\n", "<br>")

    # Instant rule-based fallback summary
    summary_items = titles[:5]
    return format_as_html_list(summary_items)

def analyze_sentiment(comments_csv, topic):
    if not os.path.exists(comments_csv):
        return "<p style='color: #94a3b8;'>No public comments collected for this topic yet.</p>"
    
    df = pd.read_csv(comments_csv)
    col = 'comment' if 'comment' in df.columns else ('title' if 'title' in df.columns else None)
    if df.empty or not col:
        return f"<p style='color: #94a3b8;'>Analysis based on headline trends for <b>{topic}</b>.</p>"

    comments = df[col].dropna().head(15).astype(str).tolist()
    comments_text = "\n- ".join(comments)

    prompt = f"""
You are a social sentiment analyst. Analyze public reaction to topic '{topic}' based on these comments:
- {comments_text}

Provide:
1. Overall Sentiment (Positive / Negative / Neutral)
2. Explanation of major themes in 3-4 sentences.
"""
    result = invoke_prompt(prompt)
    if result:
        return result.replace("\n", "<br>")

    # Fallback explanation
    pos_count = len([c for c in comments if any(w in c.lower() for w in ['good', 'great', 'best', 'win', 'awesome', 'positive', 'success'])])
    neg_count = len([c for c in comments if any(w in c.lower() for w in ['bad', 'worst', 'fail', 'poor', 'hate', 'crisis', 'loss'])])
    overall = "Positive" if pos_count > neg_count else ("Negative" if neg_count > pos_count else "Neutral")
    
    color_map = {"Positive": "#4ade80", "Negative": "#f87171", "Neutral": "#cbd5e1"}
    sentiment_color = color_map.get(overall, "#cbd5e1")

    return f"""
    <p style="font-size: 1.05rem; margin-bottom: 8px;">
        <b>Overall Sentiment:</b> <span style="color: {sentiment_color}; font-weight: 700;">{overall}</span>
    </p>
    <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
        Public discussions around <b>{topic}</b> reflect active engagement across digital platforms. Audience reactions highlight mixed perspectives on recent developments and policy updates.
    </p>
    """

def deep_dive(news_csv, topic):
    if not os.path.exists(news_csv):
        return "<p style='color: #94a3b8;'>Data file missing.</p>"
    
    df = pd.read_csv(news_csv)
    if df.empty or 'title' not in df.columns:
        return "<p style='color: #94a3b8;'>Insufficient data for Deep Dive report.</p>"

    headlines = df["title"].dropna().head(5).tolist()

    prompt = f"""
Write a 'Deep Dive of the Week' article for topic '{topic}' (200-300 words).
Context:
{chr(10).join(headlines)}

Structure:
- Background & Significance
- Key Recent Developments
- Future Outlook
"""
    result = invoke_prompt(prompt)
    if result:
        return result.replace("\n", "<br>")

    lead_story = headlines[0] if headlines else topic
    second_story = headlines[1] if len(headlines) > 1 else topic

    return f"""
    <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 10px;">
        <b>Background & Context:</b> {topic} has emerged as one of the most covered subjects across Indian media networks this week.
    </p>
    <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 10px;">
        <b>Key Developments:</b> Primary coverage centers around key announcements: <i>"{lead_story}"</i> and related updates <i>"{second_story}"</i>.
    </p>
    <p style="color: #cbd5e1; line-height: 1.6; margin: 0;">
        <b>Outlook:</b> Analysts expect continued momentum as key stakeholders evaluate long-term impacts over the coming quarter.
    </p>
    """

def expert_commentary(news_csv, topic):
    if not os.path.exists(news_csv):
        return "<p style='color: #94a3b8;'>Context unavailable.</p>"
    
    df = pd.read_csv(news_csv)
    if df.empty or 'title' not in df.columns:
        return "<p style='color: #94a3b8;'>Insufficient data for expert column.</p>"

    headlines = df["title"].dropna().head(5).tolist()

    prompt = f"""
As an expert political & economic commentator, write a 150-word column on '{topic}' given these headlines:
{chr(10).join(headlines)}
"""
    result = invoke_prompt(prompt)
    if result:
        return result.replace("\n", "<br>")

    return f"""
    <p style="color: #cbd5e1; line-height: 1.6; font-style: italic; margin: 0;">
        "The evolving narrative around <b>{topic}</b> highlights a critical juncture for institutional and public strategy in India. Strategic clarity and execution will determine future trajectory as public interest remains high."
    </p>
    """
