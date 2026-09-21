#!/usr/bin/env python3
"""comment — find hot dev.to posts worth replying to, and print the raw material.

Usage:
  python3 scripts/comment.py            # top posts by comment activity, last 2 days
  python3 scripts/comment.py -n 8       # how many candidates
  python3 scripts/comment.py --read URL # full body of one post, to draft against
  python3 scripts/comment.py --mine     # unanswered comments on OUR posts (reply first)

Output contract (what Claude turns this into): URL + an English comment. Nothing else.
No preamble, no "why I picked it", no Chinese commentary, no links to our own posts.

Ranking is by comments_count, not reactions: a busy thread is where a reply gets read,
and small active posts beat big ones because the author actually shows up.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request

UA = "WhatTechPost/1.0 (+https://github.com/frankchu91/WhatTechPost)"


def api(url, auth=False, _last=[0.0]):
    """GET with a floor on request spacing; dev.to 429s a tight loop."""
    h = {"User-Agent": UA, "Accept": "application/json"}
    if auth:
        sys.path.insert(0, "scripts")
        from publish import load_api_key
        h["api-key"] = load_api_key()
    for attempt in range(4):
        gap = time.monotonic() - _last[0]
        if gap < 1.2:                      # throttle before we get throttled
            time.sleep(1.2 - gap)
        _last[0] = time.monotonic()
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=h)))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(20 * (attempt + 1))   # back off, then retry
                continue
            raise


def strip_html(h):
    return re.sub(r"<[^>]+>", "", h).replace("&quot;", '"').replace("&#39;", "'").replace("&amp;", "&").strip()


def candidates(n=8):
    seen, rows = set(), []
    for d in (1, 2):
        for a in api(f"https://dev.to/api/articles?top={d}&per_page=40"):
            if a["id"] not in seen:
                seen.add(a["id"])
                rows.append(a)
    # skip DEV staff/meta threads — generic prompts, not technical conversations
    skip = ("devteam", "jess", "heyitsjem")
    rows = [a for a in rows if a["user"]["username"] not in skip]
    return sorted(rows, key=lambda x: -x["comments_count"])[:n]


def show_candidates(n):
    for a in candidates(n):
        print(f"\n{a['url']}")
        print(f"  @{a['user']['username']} | {a['public_reactions_count']}❤ {a['comments_count']}💬 "
              f"{a['reading_time_minutes']}m | {a['title']}")
        print(f"  tags: {', '.join(a.get('tag_list', []))}")
        body = re.sub(r"^---[\s\S]*?---\s*", "", a.get("body_markdown", "") or "")
        print("  ---")
        for line in body[:700].split("\n"):
            print(f"  {line}")


def read(url):
    path = url.split("dev.to/")[-1].strip("/")
    a = api(f"https://dev.to/api/articles/{path}")
    print(f"{a['url']}\n@{a['user']['username']} | {a['public_reactions_count']}❤ "
          f"{a['comments_count']}💬 | {a['title']}\n{'='*78}")
    print(re.sub(r"^---[\s\S]*?---\s*", "", a["body_markdown"]))
    print(f"\n{'='*78}\nEXISTING COMMENTS (do not repeat these points):")
    for c in api(f"https://dev.to/api/comments?a_id={a['id']}"):
        print(f"\n@{c['user']['username']}: {strip_html(c['body_html'])[:600]}")


def mine():
    me = "frankchu"
    for a in api("https://dev.to/api/articles/me/published?per_page=100", auth=True):
        if not a.get("comments_count"):
            continue
        cs = api(f"https://dev.to/api/comments?a_id={a['id']}")
        replied = any(c["user"]["username"] == me for c in cs)
        if replied:
            continue
        print(f"\n{a['url']}")
        for c in cs:
            print(f"  @{c['user']['username']}: {strip_html(c['body_html'])[:500]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--read" in args:
        read(args[args.index("--read") + 1])
    elif "--mine" in args:
        mine()
    else:
        n = int(args[args.index("-n") + 1]) if "-n" in args else 8
        show_candidates(n)
