<!--
REVIEW NOTES (delete before publishing)
- v2 batch, style: METHODOLOGY + REAL CODE (the mandatory technical post). REWRITTEN 2026-09-14 after the first version shipped with zero code blocks.
- Every code block below is real, from this repo: scripts/aiscan.js (the verify gate), the CLAUDE.md layer skeleton, real skill frontmatter, the promote-a-rule loop.
- Thesis: split agent instructions by change-rate; each layer needs a different mechanism (short file / dated skill + verify step / never persist).
-->

---
title: "The 3-layer split that stopped my agent's skills from rotting"
published: false
description: "My agent's instructions were one growing file that slowly went stale, and it followed the stale parts confidently. Splitting them by how often they change, and giving each layer a different mechanism, is what finally held. With the actual code."
tags: ai, agents, programming, productivity
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-14-v2-three-layer-agent-skills/cover.png
---

Last month I caught my coding agent carefully explaining how to publish a post by copy-pasting it into a website by hand. I had scripted that months earlier. But one line in its project file still described the old manual flow, and the agent followed that line with total confidence, every session. Nothing errored. It was just politely, invisibly wrong.

That is the failure mode nobody warns you about. A stale plugin crashes. A stale instruction gets **obeyed**.

The fix was not a better file. It was splitting the agent's instructions into three layers by one question, **how often does this change**, and giving each layer a different mechanism. Mixing change-rates is where all my rot came from.

## Layer 1: rules that almost never change

A short project file the agent reads every session. Conventions, commands, hard constraints. Mine is organized by the question above, not by topic:

```markdown
# Project

## HARD CONSTRAINTS        <- changes ~never; violating these is a bug
- Never publish anything about <employer> or its products.
- No AI-disclosure line on posts.

## Commands                <- changes when tooling changes
- Check a draft:  node scripts/aiscan.js drafts/<slug>/index.md
- Publish:        python3 scripts/publish.py published/<slug>/index.md --publish
- Cover image:    python3 scripts/make_cover.py --kicker ... --out drafts/<slug>/cover.png

## Layout                  <- changes when structure changes
- drafts/<slug>/index.md   gitignored, local only
- published/<slug>/        tracked; raw-URL source for images
```

The rule I enforce: **if something in here changes more than once a month, it is in the wrong layer.** Short and stable means the agent actually follows it, instead of losing three real rules inside forty.

## Layer 2: skills, which are dated procedures with a verify step

A skill is "how to do one specific task." It changes when the task changes, which is more often than the rules and far less often than a session. Two properties stopped mine from rotting.

**First: a date in the frontmatter.** A skill is a dependency, so it gets a version.

```yaml
---
name: publish-post
description: Move a draft to published/, push, then post via the dev.to API.
last_verified: 2026-09-14      # re-check when the host or tooling changes
---
```

When my tooling changes I re-verify the skills that matter, and the date tells me which ones are suspect. Without it, a skill written against a four-month-old API steers every session slightly wrong and never throws.

**Second, and this is the one that matters: every skill runs a real check on its own output.** My writing skill does not say "write in the house style" and hope. It shells out to a scanner that fails the draft on a score. Here is the actual gate, `scripts/aiscan.js`:

```js
const D = require(path.join(os.homedir(),
  '.claude/skills/avoid-ai-writing/detector/patterns.js'));

const TARGET = 2.0;                       // above this = rewrite
const text = fs.readFileSync(file, 'utf8');
const r = D.analyzeText(text);            // { score, issues[], stats }

for (const i of r.issues) {
  console.log(`  [${i.type}] ${JSON.stringify(i.text)}  => ${i.suggestion}`);
}
console.log(`  VERDICT: ${r.score > TARGET ? 'REVIEW / REWRITE' : 'PASS'}`);

process.exit(r.score > TARGET ? 1 : 0);   // <- the part that makes it a gate
```

That last line is the whole design. It exits non-zero, so the skill's procedure cannot continue past a failing draft. **A skill without a verify step is an instruction followed on faith.** The skill can be wrong, the check catches it.

## Layer 3: session context, which is never persisted

The task in front of the agent right now: the files it is touching, what I asked for, the retrieved context. This changes every session and it must not leak upward. The moment a session detail gets written into a skill "for next time," rot starts, because it was true once and will be assumed true forever.

So promotion is deliberate, never a copy-paste reflex:

```
session note  ──(true only today)──>  stays in the conversation, dies with it
              ──(true every time)──>  promote to Layer 1 rule, or a dated Layer 2 skill
```

## The loop that makes it compound

When the agent does something wrong, the reflex is to fix the output. The habit that pays is to ask **which layer failed**, then fix that:

| What went wrong | Layer | Fix |
|---|---|---|
| Broke a convention it never knew | 1 | Add one line to the project file |
| Followed an outdated procedure | 2 | Update the skill, bump `last_verified` |
| Treated last Tuesday as permanent | 3 | Pull it back out; it was a leak |

Fix the output and you fix it once. Fix the layer and it stops recurring.

## The gotcha that proves the point

My writing skill's verify step reads the **whole draft file**, including the HTML comment block at the top where I keep review notes. I had helpfully listed the words to avoid in that comment. The scanner counted them and failed the post for containing exactly the words I was telling it to avoid.

```
[tier1] "leverage"  => use
[hollow-intensifier] "genuinely"
VERDICT: REVIEW / REWRITE        # score 6, from a comment the reader never sees
```

The gate was working perfectly. I had put the test data inside the thing under test. The comment now says "avoid the swap-table words" and the list lives in a separate file, and I now assume every verify step sees more than I think it does.

Three layers, a date on each skill, a non-zero exit somewhere, and a rule that session context never gets promoted by reflex. That is the whole system, and it is the first version that has not quietly gone stale on me.

If you run agent skills: what is your verify step? I am convinced the skills without one are the ones that rot, and I want to know what other people are gating on.
