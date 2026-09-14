<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- v2 batch, style: METHODOLOGY (the mandatory substantive "方法论" post). First-hand from this repo: project file + skills + a verify gate (aiscan) + session context never persisted + the review-notes-comment gotcha + the "fix the skill not the output" loop.
- Thesis: split agent instructions into 3 layers by how often they change; most rot comes from mixing them.
-->

---
title: "The 3-layer split that stopped my agent's skills from rotting"
published: false
description: "My agent's instructions used to be one growing file that slowly went stale. Splitting them by how often they change, plus one verify step and one feedback loop, is the setup that finally held."
tags: ai, agents, programming, productivity
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-14-v2-three-layer-agent-skills/cover.png
---

For a while my agent's instructions lived in one file, and the file only ever grew. Rules, conventions, task procedures, notes from last week, a warning from an incident, all in one place. It worked until it didn't. The tell was subtle: the agent started following instructions that were no longer true, confidently, and I could not tell at a glance which parts of the file were still real.

The fix that held was not a better file. It was splitting the instructions into three layers by one question: **how often does this change?** Mixing things that change at different rates is where almost all the rot came from.

## Layer 1: rules that almost never change

The project file. Conventions, architecture, the hard constraints, the "do not touch this, removing it breaks production" notes. This layer should be short, stable, and read on every session. If something in here changes more than once a month, it is in the wrong layer.

Because it is stable, it also caches, and because it is short, the agent actually follows it instead of losing the important three rules in a wall of forty.

## Layer 2: skills, which are versioned procedures for a task

A skill is "how to do one specific thing": run the publish flow, generate a cover image, check a draft against the style guide. It changes when the task changes, which is more often than the rules but far less often than a session. Two properties made mine stop rotting.

First, every skill has a verify step, a real check it runs on its own output rather than trusting itself. My writing skill does not just "write in the house style," it runs a scanner over the draft and fails if the score is over the bar. The skill can be wrong; the check catches it. A skill without a verify step is an instruction the agent follows on faith.

Second, every skill has a date. A "last verified" line at the top, updated when I confirm it still works against the current tools. When the host changes, I re-verify the skills that matter and the date tells me which ones are stale. It is a dependency with a version, treated like one.

## Layer 3: session context, which is never persisted

The task in front of the agent right now. The files it is touching, the specific thing I asked for, the retrieved context. This layer changes every session and it must not leak upward. The moment a session detail gets written into a skill or the project file "for next time," rot begins, because it was true once and will be assumed true forever.

I am strict about this now. Per-task context stays in the conversation. If something from a session turns out to be permanently true, it gets promoted deliberately, into a rule or a skill, with a date, not copied in on impulse.

## The feedback loop that makes the layers compound

When the agent does something wrong, the reflex is to fix the output and move on. The habit that actually pays is to ask which layer failed. Did it violate a rule it did not know? Add the rule to layer 1. Did a skill's procedure go stale? Update the skill and its date. Did it act on a session detail as if it were permanent? That is a layer leak, so pull it back out.

Over a few weeks the file stopped growing randomly and started growing on purpose. Every entry is in the layer that matches how often it changes, every skill can prove it works, and nothing from a Tuesday afternoon is silently steering every session after.

One small, real gotcha from my own setup, since it is the kind of thing that only bites in practice: the scanner in my writing skill reads the whole draft, including a comment block where I had listed the words to avoid. It flagged the post for containing the words I was telling it to avoid. The verify step was working exactly as designed and I had put the test data inside the thing under test. Moving the list into a separate file fixed it, and I now assume every verify step sees more than I think it does.

If you run agent skills, how do you keep them from going stale? I have this split and a date on each one, and I still suspect I am missing a trick that someone with more skills than me has already found.
