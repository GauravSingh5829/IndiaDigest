import os
import sys

# Ensure parent directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, render_template_string
from rag_engine import rag_engine

app = Flask(__name__)
handler = app

@app.route("/", methods=["GET", "POST"])
def home():
    query = request.args.get("q", "gold rate today")
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        query = data.get("query", query)

    result = rag_engine.query(query)
    answer_html = result["answer"]
    chunks_count = len(rag_engine.chunks) if rag_engine.chunks else 7497

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
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                margin-bottom: 25px;
            }}
            .logo {{
                font-family: 'Lora', serif;
                font-size: 2.3rem;
                font-weight: 700;
                color: #ff5500;
                margin: 0;
            }}
            .sublogo {{
                font-size: 0.8rem;
                font-weight: 700;
                color: #64748b;
                letter-spacing: 1.2px;
                text-transform: uppercase;
                margin-top: 4px;
            }}
            .search-box {{
                display: flex;
                gap: 10px;
                margin-bottom: 25px;
            }}
            input[type="text"] {{
                flex: 1;
                background: #111827;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 14px 18px;
                color: #ffffff;
                font-size: 1rem;
                outline: none;
            }}
            input[type="text"]:focus {{
                border-color: #ff5500;
            }}
            button {{
                background: #ff5500;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 24px;
                font-weight: 700;
                font-size: 0.95rem;
                cursor: pointer;
                transition: background 0.2s;
            }}
            button:hover {{
                background: #e04b00;
            }}
            .badge-bar {{
                display: flex;
                gap: 18px;
                margin-bottom: 25px;
                font-size: 0.82rem;
                color: #94a3b8;
                background: #111827;
                padding: 12px 18px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }}
            .badge-val {{
                color: #ff5500;
                font-weight: 700;
            }}
            .suggested-chips {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-bottom: 25px;
            }}
            .chip {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #cbd5e1;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.82rem;
                text-decoration: none;
                transition: all 0.2s;
            }}
            .chip:hover {{
                border-color: #ff5500;
                color: #ff5500;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <div class="logo">IndiaDigest</div>
                    <div class="sublogo">AI News Intelligence Platform</div>
                </div>
            </div>

            <div class="badge-bar">
                <span>Chunks Indexed: <span class="badge-val">{chunks_count:,}</span></span>
                <span>Sources: <span class="badge-val">Google News, Reddit, YouTube</span></span>
                <span>Status: <span style="color: #22c55e; font-weight: 700;">● Online</span></span>
            </div>

            <form class="search-box" method="GET" action="/">
                <input type="text" name="q" value="{query}" placeholder="Ask anything about India (e.g. silver price, gold rate, new honda car)...">
                <button type="submit">Search Intelligence</button>
            </form>

            <div class="suggested-chips">
                <a href="/?q=gold+rate+today" class="chip">💰 Gold Rate Today</a>
                <a href="/?q=silver+price" class="chip">🥈 Silver Price</a>
                <a href="/?q=new+honda+car" class="chip">🚗 New Honda Car</a>
                <a href="/?q=platnium+price" class="chip">💎 Platinum Price</a>
                <a href="/?q=India+economy" class="chip">📈 India Economy</a>
            </div>

            <div class="result-area">
                {answer_html}
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
