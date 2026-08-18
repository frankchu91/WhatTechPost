<!--
REVIEW NOTES (delete before publishing)
- ASSETS live in drafts-assets/ (local, gitignored). On publish: move markdown to published/, move this post's PNGs to assets/, push — then the raw URLs below resolve and paste/API needs no image steps.
- All model-card facts verified first-hand on HF today (2026-08-13): license tag "qwen3.8-max", text-only, 262K native context ("extensible up to 1,010,000"), 2.4T total / 95B active, thinking mandatory. Community quotes from HF discussion #13 (no official Qwen response as of fetch time).
- Publish TODAY while the story is hot. Re-check discussions/13 for an official Qwen reply right before publishing — if one appeared, add a line.
- The Aug 15 countdown for the 27B: if it ships, that's an immediate follow-up post.
-->

---
title: "The Qwen3.8 weights are out. Last week's checklist did its job"
published: false
description: "The open release is text-only, under a custom license, with the 27B still missing. A follow-up on what verify-before-you-believe actually caught."
tags: ai, llm, opensource, machinelearning
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-13-qwen.png
---

Last week I wrote [a checklist](https://dev.to/frankchu/qwen38-max-says-it-beats-gpt-56-and-fable-5-at-computer-use-heres-my-checklist-before-i-believe-48h0) for open-weights launches, using Qwen3.8-Max as the worked example. The promised weights were "coming next week," the license was undisclosed, and I argued the right move was to wait and verify rather than celebrate.

The weights landed on Hugging Face today. I spent the morning reading the model card and the community discussion so you don't have to, and I want to walk through what the checklist caught — partly because the details matter, and partly because it's a decent case study in why boring verification beats launch-day excitement.

## What actually shipped

The repo is `Qwen/Qwen3.8-2.4T-A95B`: 2.4 trillion total parameters, 95B active per token, 512 experts with 11 activated. The architecture notes are genuinely interesting — 92 layers with a hybrid attention/linear design — and the context window is 262K native, with the card saying it's "extensible up to 1,010,000 tokens."

Then the caveats start. The open release is **text-only**. The vision capabilities that anchored the launch benchmarks — including that OSWorld computer-use score the headlines were built on — are not in these weights. Thinking mode is mandatory: the card states every response begins with reasoning and the mode cannot be disabled. And the license tag is `qwen3.8-max`, a custom scale-tiered license, not Apache 2.0.

The 27B — the model I said was the actual story for people like me — still doesn't exist. No repo, no card, no license. A countdown on ModelScope currently points at August 15.

## Scoring the checklist

**"Read the license before the model card"** — this was the checklist's first item, and it turned out to be the right instinct. Custom license, exactly the outcome the undisclosed-license smell suggested.

**"Ask which model you'd actually run"** — a 2.4T MoE was never something you or I would self-host, and that's now the release in hand while the runnable one slips. The open-weights headline and the usable artifact are different objects, and the gap between them is where launch marketing lives.

**"Give it a week of other people's traffic"** — the community found the sharp edges within hours. The top discussion thread on the repo is blunt; one user wrote that "when a model is this strong in Vision-Language tasks and you simply strip that capability away, you throw away half its core value." Another pointed out the awkwardness of tagging the repo `qwen3.8-max` while the model card treats Max features like vision and 1M context as a cloud-only tier. As of this morning there's no official response in the thread.

One thing I'll note on the other side of the ledger: 262K native context in open weights is not nothing, and neither is publishing the architecture in enough detail that the hybrid attention design can be studied. This is a real release with real value. It's just a smaller release than the launch coverage implied, in exactly the ways the checklist predicted.

## The thinking-mode detail

The mandatory reasoning mode deserves its own paragraph, because I ran into the same pattern yesterday from a different direction. I benchmarked Meta's new Muse Glimmer on my Mac this week, and its thinking turned out to be baked into the weights — ollama's `think: false` flag hides the trace without removing the cost. Now Qwen ships a flagship where thinking is mandatory by design and documented as such.

Two data points make a trend line: the current generation of open flagships assumes deliberation on every call. If your workload is high-frequency and simple — extraction, formatting, dispatch — that assumption is expensive, and it's one more reason the small-model tier of your stack isn't going anywhere.

## Where this leaves things

My plan is unchanged from last week, which is sort of the point: wait for the 27B, read its license before its benchmarks, and keep the checklist handy. If the countdown is real, we'll know by Friday whether Alibaba ships the model that actually matters for local builders — and under what terms.

If you've already got the 2.4T running somewhere serious, I'd like to hear what it took.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
