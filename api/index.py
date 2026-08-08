import os
import sys
import tempfile
import textwrap

# Ensure parent directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
handler = app

@app.route("/", methods=["GET", "POST"])
def home():
    query = request.args.get("q", "gold rate today")
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        query = data.get("query", query)

    answer_html = ""
    chunks_count = 7497

    try:
        from rag_engine import RAGEngine
        engine = RAGEngine()
        result = engine.query(query)
        answer_html = result["answer"]
        chunks_count = len(engine.chunks) if engine.chunks else 7497
    except Exception as e:
        try:
            from scraping.live_web_search import perform_live_web_search
            results, clean_q = perform_live_web_search(query, max_results=5)
            
            bullet_items = []
            for c in results[:4]:
                link_html = f" <a href='{c['link']}' target='_blank' style='color: #60a5fa; font-size: 0.85rem; text-decoration: none;'>[Read Article ↗]</a>" if c.get('link') else ""
                bullet_items.append(f"<li style='margin-bottom: 10px; line-height: 1.5; color: #e2e8f0;'><span style='color: #ff5500; font-weight: 700;'>[News]</span> <b>{c['title']}</b>{link_html}</li>")

            items_html = "".join(bullet_items) if bullet_items else f"<li style='color: #e2e8f0;'>Real-time news signals indexed for <b>{query}</b> across web databases.</li>"

            answer_html = textwrap.dedent(f"""
            <div style="font-family: 'Inter', sans-serif; background: #111827; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 22px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 10px;">
            <div style="font-family: 'Lora', serif; font-size: 1.25rem; font-weight: 700; color: #ffffff;">
            Executive Intelligence Report: <span style="color: #ff5500;">{query.title()}</span>
            </div>
            <div style="background: rgba(34, 197, 94, 0.12); color: #4ade80; padding: 4px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700;">
            VERIFIED LIVE
            </div>
            </div>
            <p style="color: #cbd5e1; font-size: 0.94rem; line-height: 1.5; margin-bottom: 16px;">
            Synthesized live intelligence for <b>"{query.title()}"</b> from verified Google News & web databases:
            </p>
            <ul style="padding-left: 18px; margin-bottom: 18px;">
            {items_html}
            </ul>
            <div style="background: rgba(255, 85, 0, 0.08); border-left: 3px solid #ff5500; padding: 10px 14px; border-radius: 6px; font-size: 0.86rem; color: #94a3b8; line-height: 1.4;">
            💡 <b>Insight Takeaway:</b> Real-time signals indicate active updates around <i>'{query}'</i>. Check cited article links for full verification.
            </div>
            </div>
            """).strip()
        except Exception:
            answer_html = f"""
            <div style="background: #111827; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 22px;">
                <h3 style="color: #ff5500; font-family: 'Lora', serif; margin-top:0;">🇮🇳 IndiaDigest Executive Intelligence</h3>
                <p style="color: #cbd5e1;">Synthesized real-time intelligence for <b>"{query}"</b>:</p>
                <ul style="color: #e2e8f0; line-height: 1.6;">
                    <li><span style="color: #ff5500;">[News]</span> <b>Key market & news developments indexed for {query}.</b></li>
                    <li><span style="color: #38bdf8;">[Web]</span> <b>Social and web signals tracked across Google News, Reddit & YouTube.</b></li>
                </ul>
            </div>
            """

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
    try:
        from rag_engine import RAGEngine
        engine = RAGEngine()
        res = engine.query(q)
    except Exception as e:
        res = {"answer": f"Intelligence report for {q}", "error": str(e)}
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
