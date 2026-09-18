<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/18 non-technical 3/3. Style: discussion. Grounded in this week's real finding: I obeyed EMDASH_MAX = 9 and BOLD_MAX = 2 for three weeks; both were dead constants, and the real thresholds were 1 (flat) and 4.
-->

---
title: "How long would you obey a rule your tooling never actually enforced?"
published: false
description: "I followed two limits in my own linter for three weeks. This week I grepped and found neither constant was ever used in a comparison. The real thresholds were different in both directions."
tags: discuss, programming, testing, career
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-18-tools-that-grade-you/cover.png
---

I found out this week that I had been obeying two rules that did not exist.

My writing checker opens with a block of constants: a maximum for one kind of punctuation, a maximum for bold phrases. I had been editing against those numbers for three weeks. Rewriting sentences. Unbolding headers. Talking myself out of punctuation, on their authority.

Then I grepped for where they were used. One is never referenced again after the line that declares it. The other appears exactly once, interpolated into a log message, never in a comparison. Neither participates in any decision the program makes.

When I measured what the tool actually enforces, both real thresholds were different from what I believed, in opposite directions. One penalty fired far earlier than the comment claimed. The other allowed more than I had been permitting myself.

So for three weeks I followed a rule that was stricter than reality in one place and looser in another, and the tool never once disagreed with me, because it was not watching that at all.

What gets me is not the bug. It is how comfortable I was. The constants sat in a block at the top of the file that looked exactly like where the tuning knobs live. They had plausible names and reasonable-sounding comments. And they had survived, which is its own kind of credential: a rule that has been there a while feels tested, when usually it just means nobody has questioned it.

I think this is a specific category of mistake and I do not have a good name for it. Not "stale config," because stale config eventually breaks something. This is config that was never wired up at all, so it can never break, so it can never be discovered by anything failing. It is only findable by someone deciding to go look, on a day when nothing was wrong.

The uncomfortable part is asking how much else in my setup is like that. A lint rule I disabled and still write around. A style guide with a limit nobody enforces. A checklist item that survives because removing it feels riskier than keeping it. I write these rules down precisely so I do not have to re-derive them, and that same property is what makes them invisible once they stop being true.

So:

1. Have you found one of these? A rule you followed that turned out to be disconnected, disabled, or never implemented. How long had it been running your behavior?
2. Do you have a habit that would catch it, or did you find yours by accident? I found mine by accident, while writing about something else, which does not feel like a system.
