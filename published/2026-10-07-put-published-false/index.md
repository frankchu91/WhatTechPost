<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 10/07 HARDCORE 2/2. All probed today against a throwaway article on my own account
  (title "scratch probe do not read ...", created published:false, left unpublished at the end).
- Measured sequence, article id 4809758:
    POST {published:false}      -> 201, url carries a "-temp-slug-7781741" suffix
                                   NOT in me/published; visible in me/all and me/unpublished
    PUT  {published:true}       -> 200, slug becomes the real one
    PUT  {published:false}      -> 200; GET /articles/{id} -> 404; public page -> 404;
                                   leaves me/published, appears in me/unpublished   (clean)
    DELETE /articles/{id}       -> 404 with an HTML error page (endpoint does not exist)
- GET /articles/{id} 404s for YOUR OWN unpublished article even with a valid key. The author-side
  view of an unpublished article is me/all or me/unpublished only. This is also why my first probe
  script died on KeyError: 'published' — the create response has no `published` field.
- I had told my own notes that removing a duplicate "needs a browser session". That was wrong and
  I never published it; correcting the record here.
- The republish path produces an inconsistent row; that is its own post (the ghost), not this one.
-->

---
title: "dev.to's API has no DELETE. It has PUT published:false, which the docs never mention."
published: false
description: "I had written off a live mistake as unfixable without a browser. Thirty minutes with a throwaway article showed the API can unpublish, and that it lies to you about your own drafts while doing it."
tags: api, python, webdev, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-10-07-put-published-false/cover.png
---

I published a post about accidentally having two copies of two articles live on my blog, and in my own notes I wrote that cleaning it up "needs a browser session, since Forem's API has no DELETE." I believed that because I had read the endpoint list, seen no delete, and stopped.

The endpoint list was right. My conclusion was not.

Before touching anything real, I made a throwaway article on my own account to probe against. That matters more than it sounds: every result below is from an article nobody was reading, which is the only responsible way to find out what a write endpoint does.

```python
body = ('---\ntitle: "scratch probe do not read"\npublished: false\n'
        'description: "api behaviour probe"\ntags: test\n---\n\nProbe article.\n')
code, data = call("POST", "https://dev.to/api/articles",
                  {"article": {"body_markdown": body}})
```

```
POST (published:false) -> 201
  id=4809758
  url=https://dev.to/frankchu/scratch-probe-do-not-read-...-51nb-temp-slug-7781741
```

Two things in that response are worth noticing before we get to the main point.

The URL carries a `-temp-slug-7781741` suffix. An unpublished article gets a placeholder slug, and the real one is assigned at publish time. So you cannot know a post's final URL before publishing it, which rules out a whole category of pre-publish link checking.

And my probe script crashed on the next line, with `KeyError: 'published'`. The create response does not contain a `published` field at all. I had assumed it would, because that is the field I sent.

## The sequence

```
PUT {published: true}    -> 200   slug becomes the real one
PUT {published: false}   -> 200
```

After the second call:

```
GET /articles/4809758        -> 404
public page                  -> 404 (gone)
in me/published              -> False
in me/unpublished            -> True
```

That is an unpublish. The article is off the internet, out of the published listing, and sitting in the unpublished one. Reversible in the sense that the row still exists and still has its content.

For completeness, the endpoint I had assumed I needed:

```
DELETE /articles/4809758  -> 404
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>404: Page ...
```

Note the HTML. A JSON API returning an HTML error page is the signature of a route that does not exist, as opposed to a route that exists and declined. Same status code, completely different meaning, and the content type is the only thing that tells you which one you got.

## The part that misled me

Look again at this pair:

```
GET /api/articles/4809758    -> 404
in me/unpublished            -> True
```

Both of those are me, with my own API key, asking about my own article. One says it does not exist. The other lists it.

`GET /articles/{id}` serves the *public* view, so it 404s on anything unpublished regardless of who is asking. There is no author mode on that endpoint. The author-side view lives at `/articles/me/all` and `/articles/me/unpublished`, and those are the only places an unpublished article of yours is visible.

Which means a 404 from that endpoint carries at least three different meanings: the article never existed, the article exists and is unpublished, or the article was deleted. You cannot tell them apart from the status code, and I had read the first meaning into a response that meant the second.

```python
def article_state(aid, key):
    """404 from /articles/{id} is not an answer. Ask the author-side endpoints."""
    for ep in ("all", "unpublished", "published"):
        rows = get(f"https://dev.to/api/articles/me/{ep}?per_page=100", key)
        hit = next((a for a in rows if a["id"] == aid), None)
        if hit:
            return ep, hit.get("published")
    return "absent", None
```

## What I am not doing with this

The obvious application is the two duplicate articles I still have live. `PUT published: false` on one copy of each would clear them, and that is a real fix available today through the API, not through a browser.

I have not run it, for a reason I found while probing further: the republish path does not come back clean. Unpublishing and then republishing the probe produced a row that two listing endpoints report as published while the public page and the single-article endpoint both return 404, stable over several minutes. So the operation is only safely one-way right now, and I would rather know exactly what the recovery path does before I use it on something real. That is the next post.

The correction I owe is smaller and more boring than any of that. I told myself a thing was impossible on the basis of an endpoint list, and the actual capability was one field in a payload I was already sending. The API documentation for Forem lists `PUT /articles/{id}` and describes it as updating an article. Unpublishing *is* updating an article. Nothing was hidden; I just read "no DELETE" as "no removal" and stopped looking.

What is the last thing you decided was impossible because the obvious endpoint for it didn't exist? I would like to know whether mine is a common shape of mistake or just a lazy afternoon.
