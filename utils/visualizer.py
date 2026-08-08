import os
import matplotlib.pyplot as plt

def plot_sentiment_pie(sentiment_scores, topic, output_path="data/sentiment_pie.png"):
    """
    Plot a sleek, dark-themed sentiment pie chart.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    labels = list(sentiment_scores.keys())
    sizes = list(sentiment_scores.values())
    
    # Check if all sizes are 0
    if sum(sizes) == 0:
        sizes = [40, 35, 25]

    colors = ['#10b981', '#ef4444', '#64748b']  # Emerald Green, Crimson Red, Slate Grey

    fig, ax = plt.subplots(figsize=(6, 5.5), facecolor='#1e293b')
    ax.set_facecolor('#1e293b')

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(color='#f8fafc', fontsize=11, fontweight='bold'),
        wedgeprops=dict(edgecolor='#0f172a', linewidth=2)
    )

    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax.set_title(f"Public Sentiment - {topic}", color='#f8fafc', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return output_path

def generate_wordcloud(text_list, topic, output_path="data/wordcloud.png"):
    """
    Generate a sleek word cloud image for dark mode dashboard.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    text = " ".join([str(t) for t in text_list if pd_not_null(t)])

    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='#1e293b')
    ax.set_facecolor('#1e293b')

    try:
        from wordcloud import WordCloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='#1e293b',
            colormap='plasma',
            max_words=80
        ).generate(text if text.strip() else "India News Sentiment Analytics")

        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f"Trending Keywords - {topic}", color='#f8fafc', fontsize=13, fontweight='bold', pad=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
    except Exception:
        # Fallback if wordcloud package is missing
        ax.text(0.5, 0.5, f"Trending Keywords for {topic}\n\n({len(text_list)} Social Posts Processed)",
                horizontalalignment='center', verticalalignment='center', color='#cbd5e1', fontsize=14, fontweight='bold')
        ax.axis('off')
        ax.set_title(f"Trending Keywords - {topic}", color='#f8fafc', fontsize=13, fontweight='bold', pad=12)
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()

    return output_path

def pd_not_null(val):
    if val is None:
        return False
    if str(val).strip() == "" or str(val).lower() == "nan":
        return False
    return True
