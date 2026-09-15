<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/14 HARDCORE 1/2. Every number below was measured on this machine today with the probe harness shown in the post.
- Key self-correction: probe A1 (1-word doc) returned score 0 and made me think scoring was density-based. Re-run at 280 words showed the opposite. The 1-word doc was the artifact.
- Real findings: dedup (5 occurrences == 1), and NO stripping of fenced code / inline code / HTML comments.
-->

---
title: "I probed my own AI-writing linter 16 ways. The first probe lied to me."
published: false
description: "I run a detector on every post before it ships. I never checked how it actually scores. Sixteen probes later I had three real answers and one embarrassing measurement error of my own making."
tags: ai, programming, testing, writing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-14-probed-my-linter-16-ways/cover.png
---

I have run an AI-writing detector on every post I publish for three weeks, changed dozens of sentences because of its output, and never once checked how it actually decides. That is a bad way to treat a tool that edits your writing. So I sat down and probed it.

The first probe told me something confidently wrong, and I believed it for about four minutes.

## The harness

Nothing clever. Write a string to a file, run the scanner, scrape the score and the flag count.

```bash
probe() {
  printf '%s' "$2" > /tmp/p.md
  out=$(node scripts/aiscan.js /tmp/p.md 2>/dev/null)
  s=$(echo "$out" | grep -oE 'score [0-9]+' | head -1)
  f=$(echo "$out" | grep -cE '^\s*\[')
  printf "%-46s %-9s flags=%s\n" "$1" "$s" "$f"
}

probe "1x leverage"   "leverage"
probe "40x leverage"  "$(python3 -c "print('leverage '*40)")"
```

The detector flags a specific set of filler words. `leverage` is on it, so it is my test particle.

## The probe that lied

```
1x leverage                    score 0   flags=0
40x leverage                   score 5   flags=1
```

One occurrence scored zero. Forty scored five. Obvious conclusion: the score is density-based, a ratio of tells to total words, and a single use is free.

I almost went and rewrote a rule in my notes based on that. Then I noticed the flaw. A one-word document is not a small version of a real document, it is a degenerate case. Any metric normalized by word count, or gated on a minimum length, will do something meaningless there. I had measured the artifact, not the behavior.

## The re-run that gave the real answer

Same probes, but padded to a realistic ~280 words first, so the document looks like a post.

```
baseline 280w, 0 tells                   score 1   flags=1
280w + 1 plain leverage                  score 3   flags=2
280w + 5 plain leverage                  score 3   flags=2
280w + 5 leverage in FENCED block        score 3   flags=2
280w + 5 leverage in HTML COMMENT        score 3   flags=2
280w + 5 leverage in inline code         score 3   flags=2
```

Three findings, all of which contradict what the first probe implied.

It deduplicates. Five occurrences cost exactly what one costs: score 3 either way. It is not density. It is "does this word appear at all," counted once per word type. Using a flagged word forty times in a real post is priced identically to mentioning it once.

It does not strip code. The word inside a fenced block scored the same as the word in plain prose. So does inline code. If you write a post about bad words and put the examples in backticks to be safe, you have done nothing.

It reads HTML comments. This is the one that had already bitten me in production without my understanding why. I keep a review-notes comment at the top of every draft, invisible to readers, and I had listed the words to avoid in it as a reminder. The scanner counted every one of them against the post. My notes to myself were failing my drafts.

## What I changed

The list of words moved out of the draft comment into a separate file the scanner never sees, and the comment now just points at it. That is the whole fix, and it took longer to diagnose than to apply.

The bigger change is how I read the number. A tool that dedups cannot tell a post that overuses a word from one that mentions it, and a tool that cannot see the difference between prose and a code block cannot tell writing from a snippet. It is a decent smoke alarm for my worst habits and a terrible judge of whether a post is any good, which is roughly what I should have assumed before I let it edit three weeks of my writing.

The part I keep chewing on is the first probe. It was not a bug, the harness worked perfectly. It answered the exact question I asked, on an input that could not possibly generalize, and it sounded authoritative doing it. My measurement was the unreliable narrator, not the tool.

Has a probe of yours ever confidently confirmed the wrong model of a system? I want the ones where the harness was correct and the input was the lie.
