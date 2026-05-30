import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from config import WEBSITES

def fetch_rss_articles(seen: dict) -> list[dict]:
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    for url in WEBSITES:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link    = entry.get("link", "")
            title   = entry.get("title", "").strip()
            summary = entry.get("summary", "").strip()

            # parse publish date
            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            # skip if older than 7 days
            if published and published < cutoff:
                continue

            # skip already seen
            if link in seen:
                continue

            articles.append({
                "url":       link,
                "title":     title,
                "summary":   summary,
                "source":    feed.feed.get("title", url),
                "published": published.isoformat() if published else "unknown",
            })

    return articles
