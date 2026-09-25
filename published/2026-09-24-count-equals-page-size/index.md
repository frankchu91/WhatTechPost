<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/24 HARDCORE 1/2. Measured today against dev.to's own API.
  per_page=5 -> 5, 30 -> 30, 60 -> 60, 100 -> 92, 200 -> 92, 500 -> 92, 1000 -> 92. True total 92.
  No total/count field in the response at all, so truncation is undetectable from one call.
- Origin: a reader (@obole) caught that a published post of mine compared a 68-post quality scan against a 60-post engagement number. Root cause was per_page=60 with no pagination. Live post already corrected and credited.
-->

---
title: "If a list endpoint returns exactly as many rows as you asked for, you have a bug"
published: false
description: "I compared 68 posts of quality data against 60 posts of engagement data and published it. A reader caught the mismatch. The cause was a page size I read as a limit, and the output was telling me the whole time."
tags: python, api, programming, testing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-24-count-equals-page-size/cover.png
---

A reader ran the numbers in one of my posts against the live API and told me they did not add up. He was right, and the tell had been sitting in my own published output for a week.

```
60 posts | 690 views | 3 reactions
```

Sixty. I had asked for sixty.

```python
mine = get("https://dev.to/api/articles/me/published?per_page=60", auth=True)
```

`per_page` is a page size, not a limit. My call took the first page and stopped, because I never wrote the loop. The quality scan earlier in that same post walked the filesystem and counted 68 files. So I compared a 68-item population against a 60-item population and presented them as one archive.

## The general shape of the tell

Any time a collection comes back with a length exactly equal to the page size you requested, treat it as truncated until you prove otherwise. Exact round numbers are not what real populations look like.

I probed the endpoint to see how visible this is:

```python
for n in (5, 30, 60, 100, 200, 500, 1000):
    r = get(f"https://dev.to/api/articles/me/published?per_page={n}")
    flag = "  <-- count == per_page" if len(r) == n else ""
    print(f"per_page={n:<5} -> {len(r):>3} returned{flag}")
```

```
per_page=5     ->   5 returned  <-- count == per_page
per_page=30    ->  30 returned  <-- count == per_page
per_page=60    ->  60 returned  <-- count == per_page
per_page=100   ->  92 returned
per_page=200   ->  92 returned
per_page=500   ->  92 returned
per_page=1000  ->  92 returned
```

The real total is 92. Every request below that came back full, and none of them said so.

That is the part worth internalising: **the response body contains no total, no count, no next-page link, and no has-more flag.** From inside a single call there is no way to distinguish "this is everything" from "this is the first slice." The only signal is the arithmetic coincidence of getting back the number you named, and that signal is easy to read straight past, because a list of the expected length looks like success.

## The fix is nine lines and I should have written them first

```python
def all_published(auth=True):
    out, page = [], 1
    while True:
        batch = get(f"https://dev.to/api/articles/me/published?per_page=100&page={page}",
                    auth=auth)
        if not batch:
            return out
        out += batch
        page += 1
```

Note the loop terminates on an empty page rather than on a short page. A short page usually means the last one, but "usually" is doing work there, and an empty page is unambiguous. The extra request costs nothing and removes a class of off-by-one-page bug.

If you want a cheap guard rather than a rewrite, assert the coincidence away at the call site:

```python
rows = get(f"{url}?per_page={n}")
assert len(rows) < n, f"got exactly {n} rows; this is a page, not a result set"
```

Ugly, and it converts a silent wrong answer into a loud wrong answer, which is the trade I want on anything feeding a number I am going to publish.

## Why this one got past me

I have a linter that checks my writing and a gate that checks my posts have real code. Neither has any opinion about whether a number in a code block is the number I think it is, and there is no tool I know of that catches "these two figures describe different populations."

What caught it was a person reading the post and re-running the query. That is the second time in two weeks someone has found a defect in something I published by executing it instead of reading it, and in both cases the bug had survived my own review completely intact.

The failure mode here is specific and worth naming. It is not that I got a wrong answer. It is that I got a **plausible** answer, with a clean round number attached, from code that ran without error. Nothing about the experience of running it suggested I should check.

So: go look at your own list calls. Grep for `per_page`, `limit`, `page_size`, `maxResults`, `top`. For each one, ask whether the code pages, and whether anything downstream would notice if it did not. I found mine in a published article, which is a worse place to find it than a code review.

What is the sneakiest truncation you have shipped? I want the ones where the number looked completely reasonable.
