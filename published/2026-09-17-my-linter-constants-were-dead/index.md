<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/17 HARDCORE 1/2. Measured today. EMDASH_MAX declared line 19, never referenced again. BOLD_MAX only referenced in a console.log string.
- Real em-dash sweep: 0 -> score 1; 1,2,3,5,9,12 -> all score 3. So the penalty fires at ONE, flat, not at 9.
- Real bold sweep: 1,2,3 -> score 1; 4,6 -> score 2 (formatting flag). So the real threshold is 4, not 2.
-->

---
title: "Two constants in my linter were dead. I obeyed them for three weeks."
published: false
description: "My checker declares EMDASH_MAX = 9 and BOLD_MAX = 2. One is never referenced again and the other only appears inside a log string. I measured what it actually enforces and both numbers were wrong."
tags: javascript, testing, programming, writing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-17-my-linter-constants-were-dead/cover.png
---

I have a script that checks my writing before I publish. It opens with a tidy block of configuration:

```js
const TARGET = 2.0;          // aim at/below this; above triggers a rewrite pass
const EMDASH_MAX = 9;        // single digits per post
const BOLD_MAX = 2;          // bold phrases per post
```

For three weeks I have edited posts against those numbers. Keep em-dashes under ten. Keep bold phrases to two. I rewrote sentences, unbolded list headers, and talked myself out of punctuation on the authority of that block.

Today I grepped for where they are used.

```
TARGET      declared line 8, used again on lines [18, 38, 46, 52]
EMDASH_MAX  declared line 19, used again on lines NEVER (dead constant)
BOLD_MAX    declared line 20, used again on lines [49]
```

`EMDASH_MAX` is never referenced after the line that creates it. `BOLD_MAX` is referenced exactly once, on line 49:

```js
console.log('  Always fix: em-dash overuse (keep single digits), bold overuse (<=' + BOLD_MAX + ').');
```

It is interpolated into a message. It is not in a comparison. Neither constant participates in any decision the program makes. The only number that does anything is `TARGET`, which gates the exit code. The other two are documentation that looks like configuration, and I had been treating them as law.

The actual scoring happens inside a detector library I call, which has its own thresholds I never looked at. So the real question is not what my constants say. It is what the library does.

## Measuring the em-dash penalty

Pad a document to a realistic length, add N em-dashes, read the score.

```bash
for n in 0 1 2 3 5 9 12; do
  python3 -c "
pad='the quick brown fox jumps over a lazy dog near the river today '*20
d=' '.join('a — b' for _ in range($n))
open('/tmp/e.md','w').write(pad+' '+d)"
  node scripts/aiscan.js /tmp/e.md | grep -E 'score .*issues'
done
```

```
 0 em-dashes -> score 1   1 issues
 1 em-dashes -> score 3   2 issues
 2 em-dashes -> score 3   2 issues
 3 em-dashes -> score 3   2 issues
 5 em-dashes -> score 3   2 issues
 9 em-dashes -> score 3   2 issues
12 em-dashes -> score 3   2 issues
```

The penalty fires at **one**, and then it is flat. One em-dash costs exactly what twelve cost. There is no "single digits are fine" behavior anywhere in this, and my comment claiming otherwise was pure invention.

That inverts the advice I had been giving myself. I had been budgeting em-dashes, spending them carefully, keeping the count respectable. The correct strategy under the actual scoring is binary: use zero, or stop counting, because the second one is free.

## Measuring the bold penalty

Same method.

```
1 bold phrases -> score 1   (no formatting flag)
2 bold phrases -> score 1   (no formatting flag)
3 bold phrases -> score 1   (no formatting flag)
4 bold phrases -> score 2   [formatting] "4 bold phrases"
6 bold phrases -> score 2   [formatting] "6 bold phrases"
```

The threshold is four, not two. Three bold phrases are free and my constant said two.

I have gone through drafts unbolding a third phrase to get under a limit that does not exist, in a file where the number I was obeying is only ever printed, never compared.

## Why this survived three weeks

The comments were plausible. "single digits per post" is a reasonable-sounding rule. The constants sat in a block at the top of the file that looks exactly like the place where the tuning knobs live. And the script kept producing verdicts that felt responsive, because `TARGET` is real and the score does move.

Nothing about the output would ever tell me that two of the three knobs were disconnected. A dead constant does not throw. It does not warn. It sits there being read by humans and ignored by the program, and the longer it sits the more authoritative it looks, because it has survived.

It is the same shape as the stale instruction problem I keep hitting with agents: a rule that is confidently followed and no longer connected to anything. Here the confident follower was me.

```js
// what the file should say
const TARGET = 2.0;   // the only number this program enforces
// thresholds for individual tells live in the detector, not here
```

If you have a config block in a script you wrote months ago, grep each name and see how many are ever read after declaration. I would bet on at least one, and I would bet you have been obeying it.
