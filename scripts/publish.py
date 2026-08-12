#!/usr/bin/env python3
"""Publish a draft to dev.to via the Forem API.

Usage:
  python3 scripts/publish.py drafts/2026-08-07-foo.md            # create as DRAFT on dev.to
  python3 scripts/publish.py drafts/2026-08-07-foo.md --publish  # publish live
  python3 scripts/publish.py drafts/2026-08-07-foo.md --dry-run  # show payload, no API call

API key: put DEVTO_API_KEY=xxx in .env at repo root (gitignored), or export it.
Get one at https://dev.to/settings/extensions -> DEV Community API Keys.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_URL = "https://dev.to/api/articles"
# dev.to's CDN blocks python's default User-Agent with 403 "Forbidden Bots".
USER_AGENT = "WhatTechPost/1.0 (+https://github.com/frankchu91/WhatTechPost)"


def load_api_key() -> str:
    key = os.environ.get("DEVTO_API_KEY")
    if not key:
        env_path = os.path.join(ROOT, ".env")
        if os.path.exists(env_path):
            for line in open(env_path):
                line = line.strip()
                if line.startswith("DEVTO_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        sys.exit("No API key. Put DEVTO_API_KEY=... in .env or export it. "
                 "Generate one at https://dev.to/settings/extensions")
    return key


def prepare_body(path: str, publish: bool) -> str:
    text = open(path, encoding="utf-8").read()

    # Strip the leading <!-- REVIEW NOTES --> comment block if present.
    text = re.sub(r"\A\s*<!--.*?-->\s*", "", text, count=1, flags=re.DOTALL)

    if not text.lstrip().startswith("---"):
        sys.exit("Draft has no front matter block; refusing to publish.")

    if re.search(r"\[PERSONAL TAKE", text):
        sys.exit("Draft still contains a [PERSONAL TAKE] placeholder. "
                 "Fill it in before publishing — that's the quality gate.")

    if publish:
        text = re.sub(r"^published:\s*false\s*$", "published: true",
                      text, count=1, flags=re.MULTILINE)
    return text


def main() -> None:
    args = [a for a in sys.argv[1:]]
    publish = "--publish" in args
    dry_run = "--dry-run" in args
    paths = [a for a in args if not a.startswith("--")]
    if len(paths) != 1:
        sys.exit(__doc__)

    body = prepare_body(paths[0], publish)
    payload = {"article": {"body_markdown": body}}

    if dry_run:
        print(body)
        print(f"\n--- dry run: would POST to {API_URL} "
              f"({'PUBLISH LIVE' if publish else 'as draft'}) ---")
        return

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "api-key": load_api_key(),
            "Content-Type": "application/json",
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    data = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.load(resp)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:  # Forem allows ~1 write per 30s
                print("rate limited (429), retrying in 35s...")
                time.sleep(35)
                continue
            sys.exit(f"dev.to API error {e.code}: {e.read().decode()[:500]}")

    print(f"OK ({'published' if publish else 'draft'}): {data.get('url', '(no url)')}")
    print(f"id: {data.get('id')}")


if __name__ == "__main__":
    main()
