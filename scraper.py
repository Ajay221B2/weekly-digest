import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from config import WEBSITES

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape_site(url: str) -> list[dict]:
    articles = []
    try:
        resp = requests.get(url, timeout=15, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        # grab all anchor tags that look like article links
        seen_titles = set()
        for tag in soup.find_all(["h1", "h2", "h3", "h4"]):
            title = tag.get_text(strip=True)
            if len(title) < 20:
                continue
            if title in seen_titles:
                continue
            seen_titles.add(title)

            # try to find closest anchor link
            link_tag = tag.find("a") or tag.find_parent("a")
            link = ""
            if link_tag and link_tag.get("href"):
                href = link_tag["href"]
                if href.startswith("http"):
                    link = href
                else:
                    from urllib.parse import urljoin
                    link = urljoin(url, href)

            articles.append({
                "url":       link or url,
                "title":     title,
                "summary":   "",
                "source":    url,
                "published": datetime.now(timezone.utc).isoformat(),
            })

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

    return articles


def fetch_rss_articles(seen: dict) -> list[dict]:
    all_articles = []
    for url in WEBSITES:
        articles = scrape_site(url)
        new = [a for a in articles if a["url"] not in seen]
        print(f"{url} → {len(new)} new articles"
