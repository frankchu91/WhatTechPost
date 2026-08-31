#!/usr/bin/env python3
"""Update an already-published dev.to article's body in place (PUT).

Usage: python3 scripts/update_live.py published/<slug>/index.md
Finds the live article whose URL matches the file's title/slug and PUTs the
new body_markdown. Reuses publish.py's key loader + body prep (strips REVIEW
NOTES, sets published: true).
"""
import json, sys, time, urllib.request, urllib.error
from publish import load_api_key, prepare_body, USER_AGENT

BASE = "https://dev.to/api/articles"


def api(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "api-key": load_api_key(),
        "Content-Type": "application/json",
        "Accept": "application/vnd.forem.api-v1+json",
        "User-Agent": USER_AGENT,
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print("rate limited (429), retrying in 35s..."); time.sleep(35); continue
            sys.exit(f"dev.to API error {e.code}: {e.read().decode()[:500]}")


def title_of(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    sys.exit("no title in front matter")


def main():
    path = sys.argv[1]
    want = title_of(path)
    # find the live article id by matching title across my published list
    page, found = 1, None
    while True:
        arts = api(f"{BASE}/me/published?per_page=100&page={page}")
        if not arts:
            break
        for a in arts:
            if a["title"].strip() == want:
                found = a; break
        if found:
            break
        page += 1
    if not found:
        sys.exit(f"no live article matches title: {want!r}")
    body = prepare_body(path, publish=True)
    res = api(f"{BASE}/{found['id']}", method="PUT",
              payload={"article": {"body_markdown": body}})
    print(f"UPDATED id {found['id']}: {res.get('url')}")


if __name__ == "__main__":
    main()
