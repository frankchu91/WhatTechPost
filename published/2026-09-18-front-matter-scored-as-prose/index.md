<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/18 HARDCORE 1/2. Measured today: identical body, score 1 -> 17 when front matter contains flagged words.
  body only: score 1, flags [low-ttr]
  body + bad front matter: score 17, flags [tier1 x7, hollow-intensifier, fnword-trigram-entropy, low-ttr]
- Same root cause as the three-checkers post but a different, sharper consequence: the scope bug inflates the score 17x.
-->

---
title: "My writing score went from 1 to 17 without touching a word of the article"
published: false
description: "Same body, same sentences. I only changed the YAML metadata at the top. The checker reads the whole file, so title and description get graded as if they were prose, and the distortion is enormous."
tags: python, testing, writing, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-18-front-matter-scored-as-prose/cover.png
---

I ran a controlled test on my writing checker this morning. Two files. The article body is byte-identical in both. The only difference is the YAML front matter above it.

```python
body = ("the quick brown fox jumps over a lazy dog near the river bank today " * 20)

# seven filler words + one hollow intensifier, spread across title and description
fm = load("fixtures/bad_front_matter.yaml")   # kept out of this file on purpose

print(score(body))       # body alone
print(score(fm + body))  # identical body, metadata on top
```

```
body only            -> score 1   flags=['low-ttr']
SAME body + bad FM   -> score 17  flags=['tier1' x7, 'hollow-intensifier',
                                        'fnword-trigram-entropy', 'low-ttr']
```

(The fixture lives in a separate file, and that is not fastidiousness. Putting those
words inline would make this article fail the very checker it is about, which is the
third time this month that has happened to me.)

One to seventeen. Seven separate filler-word flags, an intensifier flag, and an entropy flag, all raised by two lines of metadata. The prose the reader actually reads did not change at all.

## Why this is worse than it looks

My gate fails anything over 2. So a post can be perfectly clean and get blocked entirely on the strength of its own title and description, which are not prose. They are metadata: a headline and a one-line summary for a card in a feed. Different register, different constraints, different rules. A title is allowed to be punchy in ways a paragraph is not.

And the failure is silent about its cause. The report lists seven `tier1` flags with the offending words, and every one of them is in the YAML. Nothing in the output says "these came from your front matter." I have spent time re-reading a body looking for a word that was never in it.

There is a second-order effect that is subtler and worse. When the metadata is contributing most of the score, the score stops responding to the thing I am trying to improve. I could rewrite every sentence in the article and watch the number barely move, because 16 of the 17 points are sitting in two lines I was not editing. A metric that is dominated by noise is not a weak signal, it is an actively misleading one.

## The scope, again

This is the third instance of the same root cause in my pipeline this week, and at this point I have to stop calling them separate bugs. Each of my checkers reads the raw file and treats every byte as the same kind of content:

```python
raw = open(path).read()      # <- the bug, in every one of them
```

A draft file is not one thing. It is at least four:

```python
import re

def split_doc(raw):
    comments = re.findall(r"<!--[\s\S]*?-->", raw)
    body     = re.sub(r"<!--[\s\S]*?-->", "", raw)
    fm       = re.match(r"^\s*---([\s\S]*?)---", body)
    body     = re.sub(r"^\s*---[\s\S]*?---", "", body, count=1)
    code     = re.findall(r"```[\s\S]*?```", body)
    prose    = re.sub(r"```[\s\S]*?```", "", body)
    return {"comments": comments, "front_matter": fm.group(1) if fm else "",
            "code": code, "prose": prose}
```

The writing checker wants `prose` and nothing else. Not the comments, not the fenced code, and not the front matter.

## The part I am less sure about

Once I separate them, the question becomes whether the title and description should be checked at all, and I do not think the answer is "no." A description full of press-release vocabulary is a real problem, it is just a *different* problem with a different threshold. A headline gets to use a word a paragraph should not.

So the fix is not only scoping. It is scoring them separately and reporting them separately, so I can see "prose: 1, metadata: 4" instead of one number that blends two things I would act on differently.

```
prose:    score 1   ok
metadata: score 4   title/description use 7 flagged terms
```

That output would have told me in one second what took me a controlled experiment to find.

The general lesson I keep relearning this week: I built three tools that each ask a sensible question, and the bug was never in the question. It was that none of them had any idea what part of the file they were supposed to be asking it about.

If you run a linter over mixed-content files, markdown with front matter, notebooks, templated source, does it scope what it reads, or does it read the bytes and hope? Mine hoped, and a seventeen-point score on an unchanged article is what hoping costs.
