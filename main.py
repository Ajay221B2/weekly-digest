from scraper  import fetch_rss_articles
from summarizer import summarize
from delivery import send_email
from storage  import load_seen, save_seen, mark_seen, purge_old

def run():
    print("Loading seen URLs...")
    seen = load_seen()
    seen = purge_old(seen)

    print("Fetching articles...")
    articles = fetch_rss_articles(seen)
    print(f"Found {len(articles)} new articles")

    print("Summarizing with Claude...")
    digest = summarize(articles)
    print(digest)

    print("Sending email...")
    send_email(digest)

    print("Updating seen URLs...")
    for a in articles:
        mark_seen(a["url"], seen)
    save_seen(seen)

    print("Done.")

if __name__ == "__main__":
    run()
