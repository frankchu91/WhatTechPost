<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/14 non-technical 3/3. Style: contrarian opinion. Pairs with the live 3-layer technical post (22h1) — links to it.
- Real opening: the agent explaining the manual publish flow from a stale line in its project file.
-->

---
title: "Agent skills are plugins with a new name"
published: false
description: "Every host platform grows an ecosystem of installable pieces, and every one of them rots, bloats, and gets compromised. Skills will too, plus one failure mode that is worse than anything npm ever did to us."
tags: ai, agents, discuss, opensource
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-14-skills-are-plugins/cover.png
---

Last month I watched my coding agent carefully explain how to publish a post by copy-pasting it into a website by hand. I had scripted that months earlier. One line in its instructions still described the old manual flow, and the agent followed that line with complete confidence, every session, until I caught it.

Nothing errored. That is the part that stuck with me.

Here is my claim, and I would like to be talked out of it: **agent skills are plugins with a new name, and they will rot, bloat, and get compromised in exactly the ways plugins always have.** Plus one new way that is worse.

## We have run this experiment three times already

Browser extensions. IDE extensions. Package registries. Every host platform grows an ecosystem of installable pieces, and every ecosystem hits the same three walls.

They rot. The host moves, the plugin does not, and one day it does the wrong thing. Half the editor extensions I installed in 2018 are abandoned, and the ones that still technically work are the ones that worry me.

They bloat. Installing is free, so you install. Twenty extensions and a startup time you stopped noticing. Each one made sense alone.

They get compromised. A popular package changes hands, a typo-squatted name gets a few thousand installs, and something you never read is running with your permissions. We learned that lesson on npm repeatedly and are apparently ready to learn it again.

A skill is a bundle of instructions and scripts you hand your agent. Installable, shareable, mostly unaudited. I cannot find a structural reason it dodges any of the three.

## The new failure mode

A stale plugin fails loudly. It throws, it fails to load, the button does nothing, and you go look.

A stale skill fails silently, because the thing executing it is a language model that follows instructions with total confidence and no ability to notice the world moved. My agent did not flag the copy-paste procedure as suspicious. It had no way to. It was told, so it did.

Scale that to a skill written by a stranger against a version of a tool from four months ago, installed by six thousand people. It does not crash. It steers six thousand agents slightly wrong, confidently, and nobody gets an error to investigate. Silent wrongness at ecosystem scale is a new shape of problem, and we are building the distribution mechanism for it before the auditing tools.

## I am not saying don't

I use several and they earn their place. I am saying treat them as what they are, which is dependencies: know who wrote it, pin it, keep a short list, put a verify step inside the skill so it checks its own output, and re-check the important ones when the host changes. I [wrote up the structure I settled on](https://dev.to/frankchu/the-3-layer-split-that-stopped-my-agents-skills-from-rotting-22h1), and the piece that carries the weight is a date on each skill and a non-zero exit somewhere in it.

Almost nobody does this yet, which is exactly the phase where the damage accumulates unnoticed. The ecosystem is eighteen months from its first real supply-chain incident and about three years from the tooling that would have prevented it, which is the same gap we have run every previous time.

Tell me where this is wrong. Is there something about skills that actually breaks the plugin pattern, or are we early in a movie we have all seen before?
