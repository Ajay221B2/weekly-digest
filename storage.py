import json, os
from datetime import datetime, timedelta

SEEN_FILE = "seen_urls.json"

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return {}
    with open(SEEN_FILE) as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_seen(seen: dict):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

def is_new(url: str, seen: dict) -> bool:
    return url not in seen

def mark_seen(url: str, seen: dict):
    seen[url] = datetime.now().isoformat()

def purge_old(seen: dict, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    return {
        url: ts for url, ts in seen.items()
        if datetime.fromisoformat(ts) > cutoff
    }
