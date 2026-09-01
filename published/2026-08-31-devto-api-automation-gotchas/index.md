<!--
REVIEW NOTES (delete before publishing)
- FORMAT: practical/hands-on. Real bugs hit building our own dev.to publishing pipeline (publish.py + update_live.py). All first-hand.
- Walls: (1) 403 "Forbidden Bots" = default User-Agent blocked; fix custom UA. (2) 429 = ~1 write/30s; fix space + retry. (3) inline images 404 if published before pushed public; cover re-hosted but inline hot-links. Bonus: PUT /api/articles/{id} to edit live (not in quickstart).
- Complete + publish-ready, NO personal-take slot. NON-META. aiscan PASS. No AI-disclosure line.
- COVER: cover.png (HANDS-ON).
-->

---
title: "The dev.to API called my own script a bot. Three walls the docs skip"
published: false
description: "I automated publishing to dev.to and hit a 403 'Forbidden Bots' on my own key, then a silent rate limit, then broken images on a live post. All three have small fixes the quickstart never mentions."
tags: webdev, api, python, devto
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-31-devto-api-automation-gotchas/cover.png
---

I wrote a script to publish my posts to dev.to through the Forem API, using my own account and my own API key. The very first request came back `HTTP 403`, body: `Forbidden Bots`. My account, my key, calling me a bot.

The API itself is good. But three things stood between "read the quickstart" and "it actually works in a script," and none of them are in the docs. Here they are, with the fixes, so you can skip the afternoon I spent.

## Wall 1: 403 "Forbidden Bots" on a valid key

The key was fine. The problem was the User-Agent. Python's `urllib` sends `Python-urllib/3.x` by default, and dev.to's edge rejects it before your key is ever checked. A bare `curl` gets the same treatment. It looks like an auth failure and it is not.

The fix is one header. Send a real, named User-Agent and the 403 turns into a 201:

```python
HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/vnd.forem.api-v1+json",
    # the line that turns 403 "Forbidden Bots" into 201 Created:
    "User-Agent": "my-publisher/1.0 (+https://github.com/me/my-blog)",
}
```

Give it your own name and a URL. The point is just to not look like an anonymous default client. This one cost me the most time because the error points at the wrong thing.

## Wall 2: a silent rate limit at ~1 write every 30 seconds

With the UA fixed, a single post published cleanly. Then I tried to publish three in a loop, and the second and third came back `429 Too Many Requests`. Forem rate-limits writes hard, on the order of one article create or update every 30 seconds. It is not really documented, and if you batch anything you will hit it immediately.

Space your writes and retry on 429 instead of dying:

```python
import json, time, urllib.request, urllib.error

def create(body_markdown):
    payload = {"article": {"body_markdown": body_markdown}}
    req = urllib.request.Request(
        "https://dev.to/api/articles",
        data=json.dumps(payload).encode(),
        headers=HEADERS, method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:   # ~1 write per 30s
                time.sleep(35)
                continue
            raise
```

If you publish a batch, put a `sleep(35)` between posts too, not just inside the retry. A 30-second wall feels slow until you remember you are scripting away the copy-paste entirely.

## Wall 3: images that 404 on a live post

This one bites after everything looks fine. If your Markdown references an inline image by a raw GitHub URL, and you publish before that image is actually pushed and public, dev.to renders a broken image on the live post. The cover set via `cover_image:` gets re-hosted to dev.to's own CDN at publish time, so it is forgiving. Inline images hot-link to wherever you pointed them, live, every time the page loads.

So the order matters, and it is the opposite of what feels natural:

1. Push the images to the public repo first, so the raw URLs resolve.
2. Then publish the post.

Publish first and you have a live post with a broken image and a rate limit standing between you and the fix. Push first and it just works.

## Bonus: you can edit a live post, the quickstart just doesn't say so

The getting-started walks you through creating articles and stops there. But editing works: `PUT /api/articles/{id}` with a new `body_markdown` replaces the post in place, same URL, no re-publish.

```python
req = urllib.request.Request(
    f"https://dev.to/api/articles/{article_id}",
    data=json.dumps({"article": {"body_markdown": new_body}}).encode(),
    headers=HEADERS, method="PUT",
)
```

That turned "oops, typo on a published post" from a scramble into a one-line fix, and it is how I patch a post without touching its URL or its reactions.

## The whole thing, in one breath

The Forem API is a pleasure once you are past these. The trap is that all three failures point somewhere other than the cause: the 403 looks like bad auth but is the User-Agent, the 429 looks like a fluke but is a firm rate limit, and the broken image looks like a bad URL but is a timing problem. Fix the header, space the writes, push images before you publish, and the API does exactly what you want.

If you have automated your own dev.to workflow, I would like to know which edge you hit that I have not, because this list is only three deep and I doubt it is complete.
