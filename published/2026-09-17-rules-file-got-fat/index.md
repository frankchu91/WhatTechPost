<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/17 non-technical 3/3. Style: discussion. Grounded in the current real audit: CLAUDE.md is 16,230 chars / 2,524 words / ~3,281 tokens read every session, 10 sections, 108 non-empty lines, 51 rule lines, and still carries 3 mentions of a placeholder mechanism it also declares abolished.
-->

---
title: "Your agent's rules file is 3,000 tokens and half of it is archaeology"
published: false
description: "I audited the instruction file my coding agent reads every single session. It has grown to 3,281 tokens, ten sections, and rules that contradict each other because I kept appending and never deleted."
tags: discuss, ai, agents, productivity
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-17-rules-file-got-fat/cover.png
---

I audited the file my coding agent reads at the start of every session. I had not looked at it as a whole in weeks, only ever appended to it.

```
CLAUDE.md: 16,230 chars, 2,524 words, ~3,281 tokens read EVERY session
10 sections | 108 non-empty lines | 51 rule lines
```

Three thousand tokens, every session, before the agent has read a line of my actual code. That is not catastrophic on its own. What bothered me was the shape of it.

Four of the ten section headings carry a date in the title. "Revised 2026-08-31." "Added 2026-08-24." "Allowed as of 2026-09-12." Those dates are there because I kept amending rather than editing, and the honest reason is that deleting a rule feels riskier than adding one. A new rule might help. A deleted rule might be the one holding something up.

So the file grew the way a codebase grows when nobody is allowed to remove anything.

Then I grepped for contradictions and found a real one: the file mentions a placeholder mechanism three separate times, and it also states plainly that the mechanism was abolished and posts now ship complete. Both are in there. An agent reading top to bottom gets the abolition and the three references, with nothing marking which came last except dates I put in headings by accident rather than by design.

That is the part I keep chewing on. The file is not wrong, exactly. It is **stratified**. There are layers in it from different weeks, and the only reason I can read which is which is that I was there. The agent was not there. It sees one flat document where every sentence has equal authority, and the oldest instruction is often the most confidently phrased, because it has survived the longest without being questioned.

I have a theory about why this happens and I do not love what it implies. Writing a rule is cheap and feels productive. Deleting a rule requires deciding it is safe to delete, which requires knowing why it was added, which I usually do not, because I did not write down why. So the file accumulates, and the cost of the accumulation is invisible: no error, no warning, just a slowly growing preamble competing for the model's attention with the three rules that actually matter today.

The fix I am reaching for is treating it like code I can refactor, which means being willing to delete, and recording *why* a rule exists so the next me can tell whether it still applies. But I notice I am reluctant, and the reluctance is the interesting bit.

So, two questions:

1. How big is the instruction file your agent reads every session, and when did you last delete something from it rather than append?
2. Has a stale rule in yours ever produced a confidently wrong result? I want the specific case, because mine was an agent explaining a manual process I had automated months earlier, and it never once sounded unsure.
