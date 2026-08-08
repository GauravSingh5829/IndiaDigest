# 🇮🇳 IndiaDigest: GenAI-Powered Public Sentiment & Social Media Analytics

IndiaDigest is a **Generative AI news and social media analytics pipeline** that scrapes live data from **Google News, Reddit, and YouTube**, performs automated **sentiment analysis**, and generates insightful **weekly digest summaries** using **GenAI (LangChain / OpenAI / Gemini / Ollama)**.

---

## ✨ Features

- 🔍 **Multi-Source Data Scraping**
  - **Google News**: Real-time RSS feeds for national news headlines & summaries.
  - **Reddit Posts**: Top posts & discussion threads from `r/india`.
  - **YouTube Comments**: Public reactions & comment threads on trending videos.

- 📊 **Automated Sentiment Engine**
  - TextBlob polarity classification (Positive, Negative, Neutral).
  - Categorized per news headline, Reddit title, and YouTube comment.

- 🧠 **GenAI Summaries & Commentary**
  - Executive bullet-point news highlights.
  - Contextual public sentiment breakdown.
  - "Deep Dive of the Week" analytical report.
  - Expert commentary column.

- 📈 **Interactive Streamlit Dashboard**
  - Real-time sentiment distribution pie charts.
  - Keyword word-clouds.
  - Preset topic buttons (Lok Sabha Election, ISRO Mission, Indian Budget, Stock Market).
  - One-click live data refresh directly from the UI.

---

## 📁 Repository Structure

```
IndiaDigest/
├── data/                       # CSV outputs & generated charts
├── scraping/                   # Scraper modules
│   ├── google_news_scraper.py
│   ├── reddit_scraper.py
│   └── youtube_scraper.py
├── sentiment/                  # Sentiment analysis modules
│   ├── analyzer.py
│   ├── news_sentiment.py
│   ├── reddit_sentiment.py
│   └── youtube_sentiment.py
├── genai/                      # GenAI summarizer & LLM integration
│   └── summarizer.py
├── utils/                      # Visualizer & chart generation
│   └── visualizer.py
├── config.py                   # Environment configuration loader
├── main.py                     # CLI Pipeline Runner
├── streamlit_app.py            # Streamlit Dashboard UI
├── requirements.txt            # Python Dependencies
├── .env.example                # Template for environment variables
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional for API Keys)
Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```
*(Note: Google News RSS and TextBlob Sentiment work out-of-the-box without requiring API keys!)*

### 3. Run the Data & Sentiment Pipeline (CLI)
```bash
python main.py
```
Or run for custom topics:
```bash
python main.py --topics "Technology" "Healthcare" "Cricket"
```

### 4. Launch the Interactive Dashboard
```bash
streamlit run streamlit_app.py
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Data Scraping**: `feedparser`, `praw`, `google-api-python-client`, `requests`
- **Data Processing**: `pandas`, `textblob`
- **GenAI / LLM**: `langchain`, `openai`, `ollama`
- **Visualization**: `matplotlib`, `seaborn`, `wordcloud`
- **Frontend App**: `streamlit`
