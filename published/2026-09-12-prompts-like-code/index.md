<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 3 (9/12), post 1/3. FORMAT: practical/evergreen AI-building practice. Broad.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "Treat your prompts like code: version them, test them, review them"
published: false
description: "The prompt is often the most important and least engineered artifact in an AI app. It lives in a string literal, changes without review, and breaks silently. Here's the discipline that fixes that."
tags: ai, llm, programming, productivity
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-12-prompts-like-code/cover.png
---

In most AI apps the prompt is the single most important artifact and the least engineered one. The code around it gets tests, reviews, and version control. The prompt lives in a string literal or a dashboard text box, gets edited on a hunch, and ships without anyone diffing what changed. Then behavior shifts and nobody can say why. The fix is not a better prompt. It is treating the prompt the way you already treat code.

## Version it

A prompt change is a behavior change, so it belongs in git with everything else. Put prompts in their own files, not buried in string literals scattered through the codebase, and commit edits with a message that says why you made them. "Loosened the tone instruction because support replies read as robotic" is the kind of note that saves you an hour six weeks later when you are trying to remember what you were thinking. A prompt pasted into a dashboard and edited in place has no history, and a change you cannot diff is a change you cannot undo with confidence.

## Test it

This is the habit that matters most and the one almost nobody has. A prompt edit that fixes the case in front of you will, often enough to hurt, break two cases you were not looking at. The only defense is a small set of examples, a handful of inputs paired with what a good output looks like, that you run before and after a prompt change. It does not need a framework. A dozen cases in a file and a script that checks each one catches the regressions that a single hand-test never will. Without it, every prompt edit is a guess that looked fine on one input.

## Review it

"Improved the prompt" deserves a second set of eyes exactly as much as "improved the parser," because it carries the same risk of a subtle regression and usually carries less scrutiny. Put prompt diffs in the pull request. Let a teammate see what changed. The fact that a prompt reads like plain English fools people into thinking its effects are obvious, and they are not: a three-word change to a system prompt can shift the behavior of every request that flows through it.

## Trace it

Log which prompt version produced which output. When a regression shows up in production, the first question is "what changed," and if the answer lives in someone's memory instead of a version tag attached to the output, you are debugging blind. Pin the prompt per route rather than editing a shared one that silently changes five flows at once, and record the version alongside the result so a bad output points back at the exact text that produced it.

None of this is heavy. Files instead of literals, a dozen test cases, a diff in the PR, a version tag in the logs. It is the same discipline you already apply to code, pointed at the artifact that in an AI app often matters more than the code. The teams that skip it are not moving faster. They are just finding out about their regressions from users instead of from a test.

If you version and test your prompts already, I want to hear how, because the tooling here is young and everyone seems to have rigged up something slightly different.
