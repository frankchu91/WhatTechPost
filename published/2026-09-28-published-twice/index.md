<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/28 HARDCORE 1/2. Found today by an audit script on its first run. All numbers from the live API.
  92 articles live, 90 distinct titles. Two titles have two articles each.
  2026-08-31 batch, intended 3 posts, created 5 articles:
    03:30:03 id 4532381 OpenHands   10 views
    03:30:39 id 4532387 DeepSeek    20 views
    03:54:51 id 4532489 OpenHands   10 views   <- duplicate
    03:55:26 id 4532492 DeepSeek    20 views   <- duplicate
    03:56:02 id 4532498 two-agent post (the one that failed the first time)
  Gaps: 1487s and 1488s — within one second of each other, so one batch re-run.
  Bodies byte-identical (5710 vs 5710; 5130 vs 5130). Both copies of each: 0 reactions, 0 comments.
  Views split evenly: 10/10 and 20/20.
  Undetected for 24 days because every downstream check counted files, not articles.
  Re-verified 2026-10-04: both duplicates STILL live, now 34 days. View splits unchanged at
  20/20 and 10/10, both copies still 0 reactions / 0 comments. Day count updated throughout.
-->

---
title: "I published the same two posts twice and didn't notice for a month"
published: false
description: "A retry after a partially failed batch created duplicate articles with different URLs. The API has no idempotency key, and nothing I had built was counting articles."
tags: api, python, reliability, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-28-published-twice/cover.png
---

An audit script I wrote printed a line I had to read three times:

```
ERROR live duplicate x2 (ids 4532492, 4532387): DeepSeek raised its prices in the middle of a pric
ERROR live duplicate x2 (ids 4532489, 4532381): OpenHands takes a GitHub issue and hands back a pu
```

Two posts exist twice. Different article IDs, different slugs, different public URLs, byte-identical bodies. They went live on 31 August, I found them on 24 September, and as I write this they are both still up, thirty-four days in.

The thing that surfaced it was a one-line difference in how I counted. I had been comparing my local archive against a set of live titles, which silently collapses duplicates. The moment I counted articles instead of titles, the gap appeared:

```
articles: 92   distinct titles: 90
```

## Reconstructing the morning

The full timeline for that day, straight from the API:

```
      id  time (UTC)  views  title
 4532381    03:30:03     10  OpenHands takes a GitHub issue and hands back a pull request...
 4532387    03:30:39     20  DeepSeek raised its prices in the middle of a price war...
 4532489    03:54:51     10  OpenHands takes a GitHub issue and hands back a pull request...
 4532492    03:55:26     20  DeepSeek raised its prices in the middle of a price war...
 4532498    03:56:02     20  The 2026 coding setup isn't one agent, it's two: a frontier...
```

Three posts intended. Five articles created.

The first run at 03:30 published two of the three and then something went wrong before the third. I do not have the terminal output from that morning, but the shape is unmistakable: the write endpoint is rate limited to roughly one call per thirty seconds, my publisher spaces calls 35 seconds apart, and the first two calls are 36 seconds apart. Then nothing for 24 minutes.

At 03:54 I re-ran the batch. The gaps between each original and its copy are 1487 and 1488 seconds, within a second of each other, which is what a single re-run of the same list looks like rather than two separate mistakes.

The re-run republished everything from the top, because my script's idea of "has this been published" was reading the `published:` flag out of the file's front matter, and that flag is never written back to disk. So every post in the batch looked unpublished. Forever.

## The API has no idempotency key

```python
resp = post("https://dev.to/api/articles",
            {"article": {"body_markdown": body}})
```

That is the whole call. There is no client-supplied request ID, no `Idempotency-Key` header, no conflict on a repeated title. Two identical POSTs produce two articles and two 201s, and the second one looks exactly as successful as the first.

I want to be fair here: this is a defensible design. Platforms let people post twice on purpose, and refusing a duplicate title would be wrong more often than right. The mistake is mine, which is that I wrote a retry over a non-idempotent write and never thought the sentence "is this operation safe to repeat" while doing it.

The fix does not require anything from the API, only that the client asks before it writes:

```python
def publish_once(path, body, title):
    for a in all_published():                 # paginated; see note below
        if a["title"] == title:
            return {"skipped": a["id"], "url": a["url"]}
    return post("https://dev.to/api/articles", {"article": {"body_markdown": body}})
```

A check-then-act like this is racy in general, and for a single-operator publishing script at one write per 35 seconds, the race does not exist. What matters is that the check reads remote state rather than a local flag, because the local flag is what caused this.

Note the `all_published()`, too. If that function takes the first page and stops, it will miss an existing article and cheerfully create the duplicate you were trying to prevent, which is how one of my earlier bugs would have combined with this one.

## What it cost

Less than I feared, and in an instructive way:

```
OpenHands  views split [10, 10]  -> 20 total, best single copy 10
DeepSeek   views split [20, 20]  -> 40 total, best single copy 20
```

Both copies of both posts: zero reactions, zero comments. The views split almost perfectly in half, which is the part worth sitting with. Two URLs for the same article do not double your audience, they divide whatever traffic arrives, and they split any reactions or comments too, so neither copy ever builds the signal that makes a post visible.

For a post at my scale that difference is noise. For anything that ranks on engagement, publishing twice is strictly worse than publishing once, and it is worse in a way that looks like bad luck rather than a bug.

## Why it survived a month

This is the part I actually want to keep. I have had checks in this pipeline for weeks. Every one of them counted files.

The verification step after publishing read back the article I had just created and confirmed it was live, which it was, both times. A gate counts code blocks per file. A scan counts flagged words per file. A reconcile step compared the local directory against a set of live titles, and a set is exactly the data structure that makes this bug invisible.

There was no check anywhere that asked how many articles exist. A duplicate is not a property of any file, so a pipeline built out of per-file checks cannot see one, no matter how many checks you add.

```python
seen = {}
for a in arts:
    seen.setdefault(a["title"], []).append(a)
for title, copies in seen.items():
    if len(copies) > 1:
        yield f"live duplicate x{len(copies)}: {title}"
```

Six lines, and it found in its first run something a month of per-file checking could not.

If your deploy or publish step can be re-run after a partial failure, what happens on the second run? Mine had an answer I would have gotten wrong if you had asked me, and I wrote it.
