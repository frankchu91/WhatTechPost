<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/27 HARDCORE 1/2. All measured today with the repo's own aiscan wrapper around avoid-ai-writing.
- Controlled experiment, em-dash count fixed at 9, only neutral filler sentences added:
    filler  score issues words   em/words
      0       4      1     48      9/48
      2       9      2     78      9/78
      5       7      2    123      9/123
     10       5      2    198      9/198
     20       4      3    348      9/348
     40       3      3    648      9/648
  Same 9 em dashes: score 9 at 78 words, score 3 at 648 words.
- Real archive instance: published/2026-08-16-agent-native-rewrite-of-everything.md
    whole file: score 2, 3 issues, 930 words, "15 em dashes in 930 words"  -> PASS
    body only : score 3, 3 issues, 746 words, "11 em dashes in 746 words"  -> REVIEW
  IDENTICAL issue list. Only the denominator changed. Verdict flipped.
- Archive-wide, re-measured 2026-09-30: 100 posts, whole-file score > body-only in 40 (40%), 1 verdict flip.
  (Was 91 / 33 / 1 on 9/24. The flip is the same post both times, with IDENTICAL issue types.)
- Dilution experiment and the 10-word floor (patterns.js:1162) both re-verified 2026-09-30, unchanged.
- The fix described below is already live in scripts/aiscan.js as of 9/24, so these comparisons now
  have to be run against the raw detector rather than through aiscan.
- Dedup check: the tell-word checks are set-based (score didn't move with repetition), only the
  em-dash and bold checks are density-based. That mix is the actual bug.
-->

---
title: "My writing linter can be defeated by writing more. I measured how much more."
published: false
description: "Same nine em dashes, same two flagged words. Add 600 words of filler and the score drops from 9 to 3. The gate isn't wrong, it's two different kinds of check averaged into one number."
tags: javascript, testing, writing, tooling
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-27-beat-the-linter-by-writing-more/cover.png
---

I ran my writing checker over one of my own published posts twice: once on the whole file, once on just the body with the front matter removed. Same post. Same prose.

```
--- WHOLE FILE
    score 2  ·  3 issues  ·  930 words
    [tier1-clarity] "features"
    [em-dash] "15 em dashes in 930 words"
    [formatting] "4 bold phrases"
    VERDICT: PASS

--- BODY ONLY
    score 3  ·  3 issues  ·  746 words
    [tier1-clarity] "features"
    [em-dash] "11 em dashes in 746 words"
    [formatting] "4 bold phrases"
    VERDICT: REVIEW / REWRITE
```

Identical issue lists. Three findings both times, the same three. Different score, and the verdict crosses the threshold I use as a publish gate. The only thing that moved was the word count, because the front matter I stripped contributed some words and a couple of dashes to the denominator.

Which means the post passed my gate partly because it had a long description in its metadata.

## Isolating it

The archive case has two variables moving at once, so I built the clean version: a body with exactly nine em dashes, then neutral filler sentences appended, nothing else touched.

```python
core   = "The runner starts — then stalls — and the log says nothing — so I waited. " * 3
filler = "I read the log again and again on the same laptop with the same flags. "

for n in (0, 2, 5, 10, 20, 40):
    score(core + filler * n)
```

```
filler sentences  score  issues  words   em/words  verdict
               0      4       1     48       9/48   REVIEW
               2      9       2     78       9/78   REVIEW
               5      7       2    123      9/123   REVIEW
              10      5       2    198      9/198   REVIEW
              20      4       3    348      9/348   REVIEW
              40      3       3    648      9/648   REVIEW
```

Nine em dashes throughout. Score of 9 at 78 words, score of 3 at 648 words. A factor of three, from adding text that contains nothing the tool objects to.

Notice the issue count going the other way, 1 to 3, as the filler introduces its own mild flags. The tool is finding *more* problems and reporting a *lower* score, which is the clearest statement of what is actually going on.

## Two kinds of check in one number

I went looking for why, and the answer is that the checker is running two categories of test that do not compose.

The word-level tests are set-based. Repeating a flagged word does not increase its contribution; the tool deduplicates, so a post that uses a given stock phrase once and a post that uses it nine times score the same on that axis. I verified this separately, because I had previously concluded the opposite from a one-word test file, which turned out to be a degenerate input that told me nothing.

The em-dash and bold tests are density-based. They are explicitly ratios, and the output says so: "15 em dashes in 930 words."

Both are defensible in isolation. Density is the right model for punctuation, since nine em dashes in a 3000-word essay is a style and nine in two paragraphs is a tic. Set membership is the right model for stock phrases, since one instance of the worst offender on that list is already one too many, and saying it again does not make the post worse in any way the reader experiences.

The defect is adding them together. A single scalar compared against a single threshold means the density term can be driven arbitrarily low by padding, and once it is low enough it absorbs the set-based terms and the whole post passes. The threshold does not mean what I thought it meant, and it drifts depending on how long the post is.

## What I changed, and what I did not

What I actually shipped is narrower than the fix this problem deserves, so let me show the real thing rather than the version that would make a tidier post.

The detector gets a different input now. It used to receive the whole file. It receives the body, with three regions removed:

```js
const notes = raw.match(/^\s*<!--[\s\S]*?-->\s*/);
let rest = notes ? raw.slice(notes[0].length) : raw;

const fm = rest.match(/^---\n([\s\S]*?)\n---\n/);
const front = fm ? fm[1] : '';
let body = fm ? rest.slice(fm[0].length) : rest;

body = body
  .replace(/^```[\s\S]*?^```/gm, '')      // fenced blocks
  .replace(/^(?: {4}|\t).*$/gm, '')       // indented blocks
  .replace(/`[^`\n]+`/g, '');             // inline code

const r = D.analyzeText(body);
```

Each line is there for a measured reason. The notes are about the writing and are not the writing. The front matter is metadata whose word count distorts every ratio. And the code blocks had been quietly flagging `struct.unpack` in a Python snippet as the English word "unpack".

Metadata is not exempt, just separated. A title is the most-read sentence of any post, so title and description are scored as their own region, and a tell there fails the draft on its own rather than being averaged into a thousand words of body.

That check took two attempts, and the first one is the more useful story. I scored the title on its own, fed it a deliberately awful headline to make sure it worked, and watched it pass. The detector has this near the top:

```js
if (wordCount < 10) {
```

Titles are eight to fourteen words. My check was structurally incapable of firing on most of them, and it looked exactly like a check that was working. Scoring the title and the description together clears the floor, and they are the right pair anyway, since both are reader-facing and neither is article prose.

What I have **not** done is split the score itself. The body is still one scalar compared against one threshold, which means the density term can still be driven down by padding — just padding of actual prose now, instead of free padding from metadata. The real fix is to score the two families separately and let either fail the post, so there is no denominator to inflate at all. I know that is the right shape and I have not built it, and I would rather say so than publish a snippet of the gate I wish I had.

Across the whole archive the practical damage was small. A hundred posts, whole-file scored higher than body-only in 40 of them, one verdict flip. So this was never producing a flood of bad posts. What it was producing was a number I trusted for the wrong reason, on a gate I had stopped thinking about because it kept saying PASS.

That is the part that bothers me more than the arithmetic. I built the check, watched it pass for a couple of months, and stopped reading its output carefully. The experiment above took four minutes once I thought to run it, and I could have run it on day one.

If you have an automated quality gate on your own writing or code, when did you last try to defeat it on purpose? Mine took one line of filler, and I am fairly sure I am not the only person shipping a threshold nobody has attacked.
