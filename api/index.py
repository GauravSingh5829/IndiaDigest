import os
import sys

# Ensure root folder is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, render_template_string
from rag_engine import rag_engine

app = Flask(__name__)

# Top-level WSGI handler for Vercel
handler = app

@app.route("/", methods=["GET", "POST"])
def home():
    query = request.args.get("q", "India's economy")
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        query = data.get("query", query)

    result = rag_engine.query(query)

    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IndiaDigest - AI News Intelligence</title>
        <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,400&family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #0b0f17;
                color: #f3f4f6;
                margin: 0;
                padding: 40px 20px;
                display: flex;
                justify-content: center;
            }}
            .container {{
                max-width: 900px;
                width: 100%;
            }}
            .logo {{
                font-family: 'Lora', serif;
                font-size: 2.2rem;
                font-weight: 700;
                color: #ff5500;
                margin-bottom: 2px;
            }}
            .sublogo {{
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                letter-spacing: 1.2px;
                text-transform: uppercase;
                margin-bottom: 30px;
            }}
            .search-box {{
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
            }}
            input[type="text"] {{
                flex: 1;
                background: #111827;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 14px 18px;
                color: #ffffff;
                font-size: 1rem;
            }}
            button {{
                background: #ff5500;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 24px;
                font-weight: 700;
                cursor: pointer;
            }}
            .badge-bar {{
                display: flex;
                gap: 15px;
                margin-bottom: 25px;
                font-size: 0.82rem;
                color: #94a3b8;
            }}
            .badge-val {{
                color: #ff5500;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">IndiaDigest</div>
            <div class="sublogo">AI News Intelligence Platform (Vercel Live)</div>

            <div class="badge-bar">
                <span>Chunks Indexed: <span class="badge-val">{len(rag_engine.chunks):,}</span></span>
                <span>Sources: <span class="badge-val">Google News, Reddit, YouTube</span></span>
                <span>Status: <span style="color: #22c55e; font-weight: 700;">● Online</span></span>
            </div>

            <form class="search-box" method="GET" action="/">
                <input type="text" name="q" value="{query}" placeholder="Ask anything about India (e.g. silver price, gold rate, economy)...">
                <button type="submit">Search Intelligence</button>
            </form>

            <div class="result-area">
                {result["answer"]}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_page)

@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json(silent=True) or {}
    q = data.get("query", "India")
    res = rag_engine.query(q)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
