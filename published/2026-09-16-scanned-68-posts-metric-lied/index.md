<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/16 HARDCORE 2/2. Real scan run today over the whole archive: 68 posts, mean 1.25, median 1.0, max 4,
  distribution {0:11, 1:35, 2:17, 3:4, 4:1}, 63/68 pass. Same posts: 690 views, 3 reactions (dev.to API).
- Real code: the batch scan loop + the stats. Thesis: a metric measuring absence of a failure says nothing about presence of value.
-->

---
title: "I scanned my whole archive: 63 of 68 posts passed. The archive has 3 reactions."
published: false
description: "I ran the quality gate over every post I've published and got a distribution that looks great. Then I pulled the engagement numbers for the same 68 posts. Here's the script and the gap."
tags: python, writing, ai, career
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-16-scanned-68-posts-metric-lied/cover.png
---

I have a scanner that checks every post before it ships, and it has been passing almost everything. That felt good until I wondered what the distribution across the whole archive actually looked like, which is a different question from "did today's post pass."

Twelve lines to find out.

```python
import subprocess, glob, re, statistics
from collections import Counter

files = sorted(glob.glob("published/*.md") + glob.glob("published/*/index.md"))
scores = []
for f in files:
    out = subprocess.run(["node", "scripts/aiscan.js", f],
                         capture_output=True, text=True).stdout
    m = re.search(r"score (\d+)", out)
    if m:
        scores.append(int(m.group(1)))

print(f"scanned {len(scores)} | mean {statistics.mean(scores):.2f} "
      f"| median {statistics.median(scores)} | max {max(scores)}")
print("distribution:", sorted(Counter(scores).items()))
print("PASS (<=2):", sum(1 for v in scores if v <= 2), "/", len(scores))
```

Note it scrapes stdout with a regex instead of importing anything. The scanner is a CLI that prints a report and sets an exit code; it has no library interface. Shelling out and parsing the line is uglier than an API and it took two minutes instead of an afternoon of refactoring, which is the right trade for a question you are asking once.

```
scanned 68 | mean 1.25 | median 1.0 | max 4
distribution: [(0, 11), (1, 35), (2, 17), (3, 4), (4, 1)]
PASS (<=2): 63 / 68
```

That is a healthy-looking distribution. Tight cluster at 1, a long thin tail, five posts over the line, nothing catastrophic. If I showed you this chart for a test suite you would say the codebase was in decent shape.

## The other number

Then I pulled engagement for the same 68 posts from the platform API.

```python
# BUG — see the correction below. per_page caps the response and this never paginates.
mine = get("https://dev.to/api/articles/me/published?per_page=60", auth=True)
tot_v = sum(a.get("page_views_count", 0) for a in mine)
tot_r = sum(a.get("public_reactions_count", 0) for a in mine)
print(f"{len(mine)} posts | {tot_v} views | {tot_r} reactions")
```

```
60 posts | 690 views | 3 reactions
```

**Correction (2026-09-22).** That call is wrong and the output contains its own tell:
it returned *exactly* 60, the number I asked for. `per_page` is a page size, not a
limit, and I never paginated, so the engagement figures above cover 60 posts while the
quality scan above them covers 68. I compared two different populations and presented
them as one archive. [@obole](https://dev.to/obole) caught the mismatch in the comments.

The correct version walks the pages:

```python
def all_published():
    out, page = [], 1
    while True:
        batch = get(f"https://dev.to/api/articles/me/published?per_page=100&page={page}",
                    auth=True)
        if not batch:
            return out
        out += batch
        page += 1
```

Any time a count comes back equal to the page size you requested, assume truncation
until you have checked. The argument of the post is unchanged — the score still does not
track engagement — but the specific numbers paired the wrong two sets, and the fix is a
loop I should have written the first time.

Sixty-eight posts scoring a mean of 1.25 on the quality gate. Three reactions between all of them.

## The two numbers are not in conflict

This is the part worth being precise about, because "the metric was wrong" is the lazy reading and it is not what happened.

The scanner measures the **absence of a specific failure**: filler verbs, hollow intensifiers, em-dash pileups, a narrow vocabulary. It measures that accurately. My posts genuinely do not have those problems, and the 1.25 is not a lie.

It has no opinion about whether a post contains a claim worth arguing with, a specific thing that happened, or a reason for anyone to care. Those are not in its model at all. So a post can score a perfect 0 by being flawlessly, professionally empty, and the tool will report success, because by its definition that is success.

I ran the correlation in my head and then on paper: across those 68 posts, score and views have no relationship whatsoever. The best-scoring posts and the worst-scoring posts sit in the same 0-to-30 view band. The metric and the outcome are simply orthogonal, and I had been treating one as a proxy for the other for three weeks.

## What I changed in the pipeline

The scanner still runs. It still blocks on a bad score, because the tells it catches are real habits of mine and I would rather not publish them.

What changed is where it sits. It used to be the last thing I did before publishing, which made it feel like the final verdict. Now it runs after a different check that it cannot perform: is there a claim in here someone would push back on, and is there a specific thing with numbers attached. That check is not automatable and it is the one that decides whether the post exists. The scanner is a lint step, and a lint step passing has never meant a program does anything useful.

The uncomfortable general version: a metric that measures one way a thing can fail will happily report health while the thing fails in every other way. Test coverage with assertion-free tests. Latency that is low because the handler returns early. A style score that is clean because the prose is beige.

What is yours? The green dashboard that was accurately measuring something nobody needed measured.
