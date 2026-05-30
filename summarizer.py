import anthropic
from config import KEYWORDS

client = anthropic.Anthropic()

def summarize(articles: list[dict]) -> str:
    if not articles:
        return "No new articles found this week."

    articles_text = "\n\n".join([
        f"SOURCE: {a['source']}\nTITLE: {a['title']}\nSUMMARY: {a['summary']}\nDATE: {a['published']}\nURL: {a['url']}"
        for a in articles
    ])

    prompt = f"""You are a market intelligence analyst. Below are {len(articles)} fresh news articles from the past 7 days.

Keywords tracked: {', '.join(KEYWORDS)}

ARTICLES:
{articles_text}

Produce a weekly digest with:
1. TOP 5 DEVELOPMENTS — most impactful stories, 2-3 sentences each
2. MARKET SIGNALS — any trends, risks, or opportunities worth flagging
3. QUICK HITS — remaining notable headlines as a bullet list with URLs
4. ONE-LINE SUMMARY — single sentence overview of the week

Be concise. No filler. Use plain text formatting (no markdown)."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
