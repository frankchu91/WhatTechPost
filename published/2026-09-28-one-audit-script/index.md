<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/28 HARDCORE 2/2. scripts/audit.py written today; every number below is from real runs on this repo.
  Run 1: 103 files · 115 errors · 60 warnings — 91 of those errors were the notes false positive.
  Run 2 (file-level notes check removed, moved to the API): 28 errors. Two of them were the
    "REVIEW NOTES" substring search flagging the two posts that are ABOUT review notes.
  Run 3 (leak check scoped to a LEADING comment): 103 files · 26 errors · 60 warnings.
  Real errors found: 2 live duplicates, 4 archive files not live, 16 python blocks missing imports,
  4 posts with no cover_image.
- Re-run 2026-10-04: 106 files · 17 errors · 51 warnings. The missing-import count went 16 -> 7
  because 9 of the original 16 were in UNPUBLISHED drafts and the gate caught them before they
  shipped (patched 4 on 9/26, 5 more on 9/29). Verified that the drop is not the excerpt rule
  masking anything: 8 blocks still have a missing import, 7 ERROR + 1 WARN excerpt.
- Both duplicates are still live, 34 days as of today.
- The self-demonstrating bit is true and checked: the false positives were posts 4681025 and 4663292,
  which are the mention-vs-use post and the techcheck post.
-->

---
title: "I merged six checkers into one script. It found a real bug and committed one, on the same run."
published: false
description: "Every check in it exists because something it would have caught got published. Its first run reported 115 errors, 91 of which were its own bug, and one of which had been live for 24 days."
tags: python, testing, tooling, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-28-one-audit-script/cover.png
---

I had six separate scripts checking different things about my posts, written weeks apart, each with its own idea of what a post is. This week I found the same defect in five of them, so I spent an afternoon collapsing them into one file.

The first run reported this:

```
103 files · 115 errors · 60 warnings
```

Of those 115 errors, 91 were a bug in the script I had just written to consolidate the lesson about that exact bug. I want to walk through that, because the useful part of this exercise turned out not to be the consolidation.

## One function decides what a post is

The shared defect across the old scripts was that each one read the file as an undifferentiated blob. A markdown post is not a blob. It has a leading HTML comment where I keep private notes, a front matter block of metadata, and a body. Those three regions mean different things and almost no check should look at all three.

```python
def slice_post(raw):
    notes = LEAD_COMMENT.match(raw)
    notes = notes[0] if notes else ""
    rest  = raw[len(notes):]
    m     = FM.match(rest)
    front = m.group(1) if m else ""
    body  = rest[m.end():] if m else rest
    return {"notes": notes, "front": front, "body": body}
```

Every check now receives that dict and names the region it cares about. The em-dash density check reads `body`, because metadata is not prose and padding the word count with a long description used to move the score. The cover check reads `front`. Nothing reads `notes`, which was the entire point.

## The checks, and what each one cost me

```python
CHECKS = [check_missing_imports, check_untagged_fences, check_notes_not_leaked,
          check_no_published_flag, check_cover_ratio, check_em_dash_density]
```

`check_missing_imports` walks each Python block's AST, collects names it reads but never binds, and errors if any of them is a stdlib module. Sixteen percent of my published blocks raise `NameError` on paste for this reason.

`check_cover_ratio` reads the PNG header and demands exactly 1000x420, because covers are served through `fit=cover` and anything off-ratio gets center-cropped with no warning.

`check_no_published_flag` warns if front matter claims `published: true`. That flag is a local mirror of remote state and was wrong in 90 of 94 files.

`check_em_dash_density` computes a ratio over the body only, so the denominator cannot be inflated by metadata.

And `check_notes_not_leaked`, which is where it gets interesting.

## 91 false positives

The first version was two lines: if the file is in `published/` and still has a notes comment, that is a leak. It fired on all 91 archived files.

Every one was wrong. The publisher strips notes from the *payload*, not from the file. The archive is supposed to keep them; they are my record of what I verified. The live post is what must be clean, and a file on my disk is not evidence about a live post either way.

So the check had made the same category error as the five scripts it was replacing: it confused a region of a file with a fact about a remote system. I deleted it from the file level and moved it into the part of the script that talks to the API.

```python
for a in arts:
    if "REVIEW NOTES" in (a.get("body_markdown") or ""):
        out.append(f"ERROR review notes leaked into live post {a['id']}")
```

Run two. Twenty-eight errors, and this fired twice:

```
ERROR review notes leaked into live post 4681025: Three checkers I wrote, one bug: none of them can
ERROR review notes leaked into live post 4663292: I measured my last 10 posts: 9 had zero code block
```

Both false positives. The first is my post about checkers that cannot tell a mention from a use, which quotes a `REVIEW NOTES` block inside a fenced example. The second quotes the line of code that strips those comments.

A substring search for "REVIEW NOTES", inside a function written to prevent exactly this bug, flagged the two articles that are about the bug. I do not think I could have constructed a cleaner demonstration on purpose.

The actual fix is to check the *position*, not the presence, because a leak is specifically a notes comment where the publisher would have stripped one:

```python
for a in arts:
    if LEAD_COMMENT.match(a.get("body_markdown") or ""):
        out.append(f"ERROR review notes leaked into live post {a['id']}")
```

## What survived

```
--- reconcile
  ERROR live duplicate x2 (ids 4532492, 4532387): DeepSeek raised its prices in the middle of a pric
  ERROR live duplicate x2 (ids 4532489, 4532381): OpenHands takes a GitHub issue and hands back a pu
  ERROR published/2026-08-07-nvidia-nooa-agent-one-python-class.md: in published/ but not live on dev.to
  ERROR published/2026-08-13-qwen-weights-checklist-followup.md: in published/ but not live on dev.to
  ERROR published/2026-08-19-stripe-buys-openrouter.md: in published/ but not live on dev.to
  ERROR published/2026-08-21-anthropic-model-2-withheld.md: in published/ but not live on dev.to
  info  90 posts live on the API

103 files · 26 errors · 60 warnings
```

Two of my posts have been live in duplicate since 31 August, under different URLs, splitting their traffic. Four files sit in a directory called `published/` that were never published at all. Sixteen code blocks will not run if you paste them.

That was the run on the day I wrote the script. I re-ran it before publishing this, ten days later:

```
106 files · 17 errors · 51 warnings
```

The duplicates and the four phantom files are unchanged, which I will come back to. The interesting movement is the missing imports, 16 down to 7, and I want to account for it rather than let it read as progress I did not earn. Nine of the original sixteen were in drafts that had not shipped yet. The gate failed them, I added the import lines, and they went out correct. So that number did not improve because I cleaned up the archive; it improved because the check ran before publication instead of after, which is the only place a check of that kind is worth anything.

I did check that the drop was not the gate going quiet on me, since a check that stops firing looks identical to a problem that stopped happening. Eight blocks still carry a missing import today: seven reported as errors, one as a warning because it is a marked excerpt of real source.

The duplicates are the find I care about, because they were structurally invisible to everything I had before. A duplicate is not a property of any file. Six per-file checkers cannot see one no matter how good each of them is, and the only reason this script caught it is that `reconcile` counts articles from the API rather than reading my directory.

## The thing I would tell myself in August

Consolidating the scripts was worth doing and is not the lesson. The lesson is in the two false-positive rounds: I knew about this bug class, I had written five instances of it, I was actively writing a post about it, and I still shipped it twice more inside the tool built to fix it in one afternoon.

Knowing a failure mode does not protect you from it. What protects you is a specific mechanical question asked at the point of writing, and for this class the question is: *which region of the input is this check about, and did I extract that region or just search the whole thing?*

That question would have caught all seven instances. Understanding the use-mention distinction caught none of them, including when I was in the middle of explaining it.

What is the check in your pipeline that has never once fired? I had four of those, and two were not firing because they were structurally incapable of it.
