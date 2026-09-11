<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 1 (9/10), post 3/3. FORMAT: discussion (提问式), discuss tag. Short (~500w). Reader-first, ends on a real question.
- Distinct from prior discussion posts (agent-context, agent-optimizes-test). This one is about the merge/trust decision.
- aiscan-clean; no banned words in this comment. NON-META. No AI-disclosure line. COVER: cover.png (OPINION).
-->

---
title: "The PR is green and you didn't write a line of it. What's your actual bar for merging?"
published: false
description: "AI wrote the change, the tests pass, the diff looks plausible. Somewhere between reading every line and trusting the checks is a line you draw every day. I want to compare where people draw it."
tags: discuss, ai, agents, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-10-merge-ai-pr-discussion/cover.png
---

Here is a moment that happens to me most days now. An agent hands back a pull request. The tests are green, the diff is plausible, and I did not write a single line of it. Now I have to decide whether it merges, and I have noticed I do not actually have a consistent rule for that. I want to know if you do.

The options seem to sit on a spectrum.

At one end, you read every line as if a stranger wrote it, because a stranger did. Slow, safe, and it quietly gives back a lot of the speed the agent was supposed to buy you.

In the middle, you trust the tests and spot-check the risky parts. This is where I mostly live, and it rests on an uncomfortable assumption: that my test suite is good enough to catch what I am not reading. On the repos where that is true, it works. On the repos where the tests are thin, I am really just trusting a green checkmark and calling it review.

At the other end, you skim and merge if nothing jumps out, because the volume is too high to do more and the agent is usually right. Fast, and the failure mode is a subtle bug that was plausible enough to pass a skim, which is exactly the kind of bug these models are best at producing.

Where I have landed, for now, is that I read an agent's diff about as carefully as I would a new hire's, and I trust the tests only as far as I actually trust the tests. Which means the real work moved: the thing that decides whether I can merge quickly is how good my tests were before the agent ever ran. Verification did not get cheaper just because generation did.

But that is one person's rule, and I flip on it depending on the stakes of the repo.

So, concretely, two questions:

1. What is your actual bar for merging a change you did not write? Read every line, trust the suite, spot-check, or something else?
2. Has that bar ever burned you, a green PR that was wrong in a way you only caught later? What did it change about how you review now?

I am after the specific stories, not the principles, because I suspect most of us are improvising this and pretending we have a policy.
