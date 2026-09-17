<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/16 HARDCORE 1/2. Real code from scripts/update_live.py. Verified today against live article 4648628:
  slug preserved after PUT, edited_at 2026-09-14T08:35:06Z vs published_at 08:31:47Z, title lookup found it on page 1 of me/published.
- The quickstart documents POST only; PUT /articles/{id} is the edit path.
-->

---
title: "The dev.to API can edit a published post. The quickstart never says so."
published: false
description: "I published a post with a mistake in it and assumed the fix was manual. It isn't: PUT to the article id replaces the body in place, keeps the URL, and the reactions survive. Here's the script and what I verified."
tags: python, api, webdev, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-16-edit-live-post-put/cover.png
---

I published a post, then noticed it was missing something important. My assumption was that the API is write-once: create via POST, and anything after that happens in the web editor by hand.

That assumption cost me a few manual edits before I went looking. The API edits fine. It is just not in the getting-started path, which walks you through creating an article and stops.

## The edit call

`PUT /api/articles/{id}` with a new `body_markdown` replaces the post in place.

```python
def api(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/vnd.forem.api-v1+json",
        "User-Agent": "my-publisher/1.0",   # default UA gets a 403
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:   # ~1 write per 30s
                time.sleep(35); continue
            raise

api(f"https://dev.to/api/articles/{article_id}", method="PUT",
    payload={"article": {"body_markdown": new_body}})
```

Two headers do the unglamorous work. A real `User-Agent`, because the default Python one gets rejected at the edge before your key is ever checked, and the retry on 429, because writes are rate limited hard enough that a small batch will hit it.

## Finding the id without storing it

My drafts live in git, not in a database, so I do not have the article id lying around. The lookup is a scan of your own published list, matched on title:

```python
def find_id_by_title(title):
    page = 1
    while True:
        arts = api(f"https://dev.to/api/articles/me/published?per_page=100&page={page}")
        if not arts:
            return None
        for a in arts:
            if a["title"].strip() == title:
                return a["id"]
        page += 1
```

Crude, and fine at my volume. Verified just now: the lookup found the post on page 1, because `me/published` is newest-first and the thing you want to fix is almost always recent.

## What I verified after the PUT

The questions I actually had were about what an edit does to a live post, so I checked the article back:

```
slug still:   the-3-layer-split-that-stopped-my-agents-skills-from-rotting-22h1
edited_at:    2026-09-14T08:35:06Z
published_at: 2026-09-14T08:31:47Z
body has code blocks: 5
```

**The URL survives.** The slug is unchanged after the edit, so links you have shared, and any cross-links from your other posts, keep working. This is the one that mattered to me, because a fix that rewrites the URL is not a fix.

**`edited_at` and `published_at` are separate fields.** The publish time stays put and the edit gets its own timestamp. Your post does not jump back to the top of anything and does not pretend it was never wrong.

**Reactions and comments are attached to the article, not the body.** Replacing the body does not touch them.

## The one sharp edge

`body_markdown` is a full replacement, not a patch. Whatever you send becomes the entire post. So the safe flow is: keep the markdown in git as the source of truth, edit the file, send the file. If you ever hand-edit in the web editor and then PUT from your local copy, you silently discard the web edit.

That is the actual reason to script this rather than use the editor: not speed, but having one place the post really lives. Mine is a folder in a repo, the local file is authoritative, and `update_live.py` is the one-way valve that pushes it up.

```
$ python3 scripts/update_live.py published/<slug>/index.md
UPDATED id 4648628: https://dev.to/frankchu/the-3-layer-split-...-22h1
```

Typos on published posts went from a chore I avoided to a one-liner I run without thinking, which mostly means I now fix things I would previously have left wrong.

If you automate your own publishing, do you treat the remote as authoritative or the repo? I went with the repo and the full-replacement semantics made that decision for me.
