<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/26 HARDCORE 1/2. Re-measured 2026-09-26 (the 9/24 numbers had already drifted).
  94 files in published/.  Every single one has front matter `published: false`.  90 are live on dev.to.
  Cross-tab:  published:false & live=True -> 90 ;  published:false & live=False -> 4.
  Flag agrees with reality in 4 of 94 files, and only by accident.
  The three posts published on 9/24 still say `published: false` on disk — the bug reproduced live.
- Root cause confirmed by reading publish.py lines 55-57: the `published: true` rewrite is
  `text = re.sub(...)` on the in-memory string that becomes the payload. Nothing is written back to disk.
- The 4 non-live files were moved into published/ by commits whose messages start with "Publish:".
  Commit message, directory name, and front-matter flag all disagree with the API.
-->

---
title: "I have the same boolean in 94 files. It is wrong in 90 of them."
published: false
description: "Every archived post in my repo says published: false. Ninety of them are live. The bug is one line that looks like it mutates state and doesn't."
tags: python, programming, testing, devops
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-26-boolean-wrong-90-times/cover.png
---

I was reconciling my blog archive against the API and printed a cross-tab I expected to be boring:

```
files in published/           : 94
  front matter published:true : 0
  front matter published:false: 94
  actually live on dev.to     : 90
```

Zero. Not a few stragglers. Every file in the directory named `published/` declares that it is not published, and 90 of them have been live for weeks. The flag matches reality in 4 files out of 94, and it does that by being wrong in the same direction as four posts that never shipped, which is not agreement so much as a broken clock.

## The line

```python
# scripts/publish.py, inside prepare_body(). `import re` is at the top of the module.
if publish:
    text = re.sub(r"^published:\s*false\s*$", "published: true",
                  text, count=1, flags=re.MULTILINE)
return text
```

That is from the function that prepares a post before sending it. The regex is correct. The flag is correct. The payload that goes to the API is correct, which is exactly why every post actually published fine and nothing ever alerted me.

`text` is a local string holding a copy of the file. The substitution rewrites the copy. The copy becomes the request body. The file on disk is never opened for writing, in this function or anywhere else in the script. Everything about the line reads like a state change, including the verb in `re.sub`, and it is a pure transformation of a value that is about to be thrown away.

So the on-disk flag does not record whether a post is published. It records what the file said before a publish attempt, forever, regardless of outcome.

## Four sources of truth, in descending order of authority

What made this worth more than a one-line fix is how many things in my repo were confidently claiming to know the answer.

```
published/2026-08-21-anthropic-model-2-withheld.md
    first commit : 632076f "Publish: Anthropic Model 2 post + cover + CoBench chart"
    directory    : published/
    front matter : published: false
    live on API  : NO
```

The commit message says Publish. The directory says published. The flag says false. The API, which is the only one of the four that actually knows, says the post does not exist. Three of my four signals are derived from my intent at the moment I ran a command, and none of them from the result.

That post is not live, by the way. I do not know why. The commit from that day shows the file moved and the images added, so the most likely story is that the API call failed or was never made after the move, and every subsequent tool I wrote believed the directory.

## The check that should have existed on day one

```python
import glob

def reconcile():
    live = {a["title"] for a in all_published_from_api()}
    for path in glob.glob("published/**/*.md", recursive=True):
        fm = front_matter(path)
        on_disk = fm.get("published") == "true"
        on_api  = fm.get("title") in live
        if on_disk != on_api:
            yield path, on_disk, on_api
```

Eleven lines, and running it today is what produced every number in this post. I did not write it for two months because the archive felt like it was self-describing. The file is in `published/`, so obviously it is published.

There is a decent argument that the flag should not exist on disk at all. It is a request parameter for the API, not a property of my file, and duplicating remote state into a local file is how you end up with a field nobody updates. The version I am moving to keeps the flag out of the archive entirely and derives live status from the API when anything needs it, with a small cache.

But I want to name the failure more precisely than "don't duplicate state", because I would have agreed with that advice and still written this bug. The specific trap is that `re.sub` on a variable you are about to send is indistinguishable, at a glance, from `re.sub` on a variable you are about to save. Same function, same shape, same line. The difference lives entirely in what happens to the result three lines later, and when I read that function back during review, I read the intent rather than the data flow.

The two greps I ran on the rest of the repo afterwards:

```
rg 're\.sub|\.replace\(' --type py -A3 | rg -v 'open\(|write\(|Path\('
```

Any in-place-looking string transform with no write nearby. And the one that found the second instance:

```
rg 'def \w+\(.*path' -A20 --type py | rg 'return (text|body|content|data)'
```

A function that takes a path, transforms, and returns instead of persisting. Two of those were fine and one was the same bug in a cover-image script.

## What I actually changed

The fix is not writing the flag back. If I did that, I would have a boolean that is correct at publish time and starts rotting immediately, because a post can be unpublished or deleted on the platform without my repo hearing about it. Local mirrors of remote state have exactly one correct value, which is the value at the moment you last synced, and they never say when that was.

So the archive stops claiming. The reconcile function runs as a check, it prints disagreements, and the API stays the only thing that gets to answer the question.

If you have a field in your repo that mirrors a remote system's state, when did you last verify it? Mine went 94 files deep before I thought to ask, and I only asked because I was looking for something else.
