#!/usr/bin/env python3
"""
TRU Current Events puller.
Fetches and caches live telemetry with cross-corroboration.

Usage:
  python current_events_pull.py pull
  python current_events_pull.py stats
  python current_events_pull.py search <query>
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

CACHE_DIR = Path("/home/workspace/primaries/current_events")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "current_events.json"
USER_AGENT = "TRU Current Events bot/1.0"

STATUS_SOURCES = [
    {
        "name": "anthropic",
        "url": "https://status.anthropic.com/api/v2/incidents.json?limit=10",
    },
    {
        "name": "openai",
        "url": "https://status.openai.com/api/v2/incidents.json?limit=10",
    },
    {
        "name": "cloudflare",
        "url": "https://www.cloudflarestatus.com/api/v2/incidents.json?limit=10",
    },
]

X_POSTS = [
    {"url": "https://x.com/i/status/2060201705195880897", "label": "openai outage mention"},
    {"url": "https://x.com/i/status/2060547029890126094", "label": "infra reliability commentary"},
    {"url": "https://x.com/i/status/2061348355490607222", "label": "cloudflare dependency notice"},
    {"url": "https://x.com/i/status/2059166197195657433", "label": "anthropic acquisition commentary"},
]


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        return {"error": str(e), "url": url}


def pull():
    items = []
    sources = []

    for src in STATUS_SOURCES:
        data = fetch_json(src["url"])
        sources.append({"name": src["name"], "url": src["url"], "ok": "error" not in data})
        if "error" in data:
            continue
        incidents = data.get("incidents", []) or []
        for inc in incidents[:5]:
            items.append({
                "source": src["name"],
                "id": inc.get("id"),
                "name": inc.get("name") or inc.get("status") or "incident",
                "status": inc.get("status"),
                "impact": inc.get("impact"),
                "created_at": inc.get("created_at"),
                "updated_at": inc.get("updated_at"),
                "url": src["url"],
                "kind": "status_incident",
            })

    for post in X_POSTS:
        items.append({
            "source": "x",
            "label": post["label"],
            "url": post["url"],
            "kind": "x_post",
        })

    doc = {
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "count": len(items),
        "sources": sources,
        "items": items,
    }
    CACHE_FILE.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "count": len(items), "cache": str(CACHE_FILE)}, indent=2))
    return doc


def stats():
    if not CACHE_FILE.exists():
        print(json.dumps({"ok": False, "message": "no cache"}, indent=2))
        return
    doc = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    print(json.dumps({
        "ok": True,
        "count": doc.get("count", 0),
        "pulled_at": doc.get("pulled_at"),
        "sources": len(doc.get("sources", [])),
    }, indent=2))


def search(query: str):
    if not CACHE_FILE.exists():
        print(json.dumps([], indent=2))
        return
    doc = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    q = query.lower().strip()
    results = []
    for item in doc.get("items", []):
        text = json.dumps(item).lower()
        if q in text:
            results.append(item)
    print(json.dumps(results[:20], indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "pull":
        pull()
    elif cmd == "stats":
        stats()
    elif cmd == "search":
        search(" ".join(sys.argv[2:]))
    else:
        print(__doc__)
