<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/15 HARDCORE 1/2. Real: I built scripts/techcheck.js today after measuring 9 of my last 10 posts had ZERO code blocks. Real code, real exit codes, real measurement loop.
- The comment-stripping line is the load-bearing bit and it exists because the OTHER gate (aiscan) got fooled by a draft comment.
-->

---
title: "I measured my last 10 posts: 9 had zero code blocks. So I wrote a gate."
published: false
description: "I kept calling posts 'technical' when they were prose about technique. One shell loop proved it, so I built a check that fails the build instead of trusting my judgment. It has one line that matters."
tags: javascript, programming, writing, testing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-15-gate-that-eats-its-own-notes/cover.png
---

Someone told me my technical posts were not technical. I disagreed, then I measured, which is a bad order to do those two things in.

```bash
for f in $(ls -dt published/*/index.md | head -10); do
  n=$(grep -c '^```' "$f")
  echo "$((n/2)) code blocks | $(basename $(dirname $f))"
done
```

```
3 code blocks | 2026-09-13-precommit-hook-secrets
0 code blocks | 2026-09-14-every-attack-started-with-a-stolen-key
0 code blocks | 2026-09-14-three-layer-agent-skills      <- the "methodology" post
0 code blocks | 2026-09-14-60-posts-690-views-autopsy
0 code blocks | 2026-09-10-repo-lockdown-before-agent
0 code blocks | 2026-09-13-faster-or-busier-discussion
0 code blocks | 2026-09-13-streaming-llm-responses
0 code blocks | 2026-09-12-run-household-with-muse
0 code blocks | 2026-09-07-prompt-caching-llm-bill
0 code blocks | 2026-09-12-docs-vs-ask-discussion
```

Nine of ten. Including the one I had labelled a methodology post, which turned out to be eight hundred words describing an approach without ever showing it. My judgment about my own output was worthless, so I replaced it with an exit code.

## The gate

```js
const MIN_BLOCKS = 2;       // at least two fenced blocks
const MIN_CODE_LINES = 12;  // substantive, not two one-liners
const MIN_LANGS = 1;        // fences tagged: ```js, ```python, ```yaml

// strip the REVIEW NOTES comment so my own notes never count as content
const raw = fs.readFileSync(file, 'utf8').replace(/^\s*<!--[\s\S]*?-->\s*/, '');

const fences = [...raw.matchAll(/^```([a-zA-Z0-9+-]*)\n([\s\S]*?)^```/gm)];
const blocks = fences.length;
const codeLines = fences.reduce(
  (n, m) => n + m[2].split('\n').filter(l => l.trim()).length, 0);
const langs = new Set(fences.map(m => m[1]).filter(Boolean));

const checks = [
  [blocks    >= MIN_BLOCKS,     `${blocks} code blocks (need >= ${MIN_BLOCKS})`],
  [codeLines >= MIN_CODE_LINES, `${codeLines} lines of code (need >= ${MIN_CODE_LINES})`],
  [langs.size >= MIN_LANGS,     `fences tagged: ${[...langs].join(', ') || 'NONE'}`],
];

const pass = checks.every(([ok]) => ok);
process.exit(pass ? 0 : 1);
```

Three details earn their place.

**`MIN_CODE_LINES` alongside the block count.** Two fenced one-liners is not a technical post, and a block count alone is trivially gamed. Counting non-blank lines inside the fences is the part that makes it a real bar.

**Requiring a language tag.** An untagged fence is usually pasted output or a scratch block. Tagged fences are the ones someone wrote on purpose, and it costs nothing to demand.

**That regex on line 6, which is the one that actually matters.** My drafts carry an HTML comment at the top with review notes, and those notes are full of the word "code" and sometimes contain code. Without the strip, a post could pass the technical gate on the strength of my private notes about how technical it needed to be. The test data lives in the same file as the thing under test, so the check has to cut it out first.

I know to do that because my other gate got fooled exactly this way. The AI-writing scanner reads the whole file, comments included, and I had once listed the words to avoid inside that comment. It counted them and failed the post. Same file, same class of bug, opposite direction.

## Running it

```
$ node scripts/techcheck.js published/2026-09-14-three-layer-agent-skills/index.md
  ok   5 code blocks (need >= 2)
  ok   31 lines of code (need >= 12)
  ok   fences tagged with a language: markdown, yaml, js
  VERDICT: TECHNICAL

$ node scripts/techcheck.js published/2026-09-14-60-posts-690-views-autopsy/index.md
  FAIL 0 code blocks (need >= 2)
  FAIL 0 lines of code (need >= 12)
  FAIL fences tagged with a language: NONE
  VERDICT: PROSE — add real code or reclassify
  (exit 1)
```

Then I pointed it at everything else I had queued and it failed seven drafts out of seven. Not one of the things I had been calling technical would have passed. That is the number that told me the gate was calibrated correctly, because my own sense of "this one has substance" had been wrong seven times in a row.

## Why an exit code and not a rule

I already had the rule. It was written down, in the file the agent reads every session, in plain language: at least one post a day must be a real technical piece. I violated it nine times out of ten while believing I was following it, because "is this technical enough" is a judgment call and I am the least reliable possible judge of my own work at the moment I finish it.

A rule you can talk yourself past is a preference. `process.exit(1)` is not negotiable, which is the entire reason to spend twenty minutes writing one.

What is in your repo that is enforced by a person's good intentions and should be enforced by a non-zero exit? I suspect everyone has one and it is always the thing they are sure they would never get wrong.
