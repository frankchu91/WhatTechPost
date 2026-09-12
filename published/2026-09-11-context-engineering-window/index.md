<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 2 (9/11), post 1/3. FORMAT: practical/evergreen AI-building. General principles (no hard numbers to go stale). Distinct from the caching post: this is about WHAT goes in context (relevance), not cache mechanics.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "Context engineering is mostly deciding what to leave out"
published: false
description: "The instinct is to stuff more into the window. But irrelevant context makes the model worse and costs you on every turn. The skill is subtraction, not accumulation."
tags: ai, llm, programming, machinelearning
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-11-context-engineering-window/cover.png
---

Most advice about context windows is about fitting more in. Bigger windows, more retrieved documents, the whole file instead of the function. In practice the thing that has improved my results the most is the opposite move: getting the junk out. A window packed with marginally relevant material makes the model answer worse, not better, and you pay for every token of it on every turn.

## More context is not more signal

A model does not read your context the way a search index does, weighting only what matches. It attends across everything you gave it, and irrelevant material competes for that attention. Feed it five retrieved chunks when one is relevant, and you have not added four data points, you have added four chances for the model to anchor on the wrong thing and four distractions from the one that mattered. Long contexts also have a well-known soft spot in the middle: material at the very start and the very end gets weighted more than material buried in between, so where a fact sits changes whether it gets used.

The result is that a smaller, sharper context usually beats a larger, noisier one, even when the large one technically contains the answer.

## What earns a place in the window

I think of it as three piles. The task itself, stated plainly. The few facts that actually bear on this task, and only those. And the shape of the output you want. Almost everything else is a candidate for cutting.

What I find myself removing most often: the entire file when twenty lines are relevant, the full conversation history when the last two turns carry the thread, boilerplate headers and license blocks that came along for the ride with a retrieved snippet, and documents that a retriever scored as "close" but a human would call off-topic. Retrieval gets you candidates. Trimming them to the ones that earn their place is the part that decides answer quality.

## Placement is a lever too

Since the start and end of a long context get the most attention, put the material that matters there. The instruction and the most relevant facts belong near the end, next to the question, not stranded in the middle of a wall of retrieved text. If you are assembling a prompt from many sources, order them by how much they bear on the task, not by the order your pipeline happened to fetch them.

## The cost side is the same lesson

Every token you put in the window is a token you pay for, and in a multi-turn agent you pay for it again on every subsequent call as the history grows. So junk context is expensive twice: once in dollars and once in quality. That makes trimming one of the few moves that improves the answer and lowers the bill at the same time, which is rare enough to be worth reaching for first.

The practical version is a short loop. Retrieve generously, then re-rank and cut to the few pieces that actually matter. Summarize long history instead of resending it raw. Strip boilerplate before it enters the prompt. And when an answer comes back wrong, check what you put in the window before you reach for a bigger model, because often the fix is not more context but less of the wrong context.

If you have cut something from a prompt and watched the output get better, I want to hear what it was, because those subtractions are the least-documented part of building with these models.
