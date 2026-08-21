<!--
REVIEW NOTES (delete before publishing)
- COVER IMAGE: assets/2026-08-20-ultrafast.png
- Optional chart: tok/s comparison (normal Sol vs Ultrafast ~750). assets/2026-08-20-ultrafast-chart.png
- Facts (research/2026-08-19-topic-scan.md): limited API preview of Ultrafast mode for GPT-5.6 Sol, powered by Cerebras, ~750 output tok/s, up to 14x faster. Confirm preview access terms the day you publish.
- Angle is about latency×steps in agent loops, not raw speed bragging.
-->

---
title: "750 tokens a second changes what an agent can do, not just how fast it feels"
published: false
description: "OpenAI's Ultrafast mode for GPT-5.6 Sol, on Cerebras hardware, hits ~750 tok/s — up to 14x faster. The interesting part isn't the demo, it's the loop."
tags: ai, llm, performance, agents
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-20-ultrafast.png
---

OpenAI opened a limited preview this week of an "Ultrafast" mode for GPT-5.6 Sol, running on Cerebras hardware, clocking around 750 output tokens per second — up to 14x faster than standard. It's easy to file this under "nice, faster chat" and move on. I think that undersells what changes.

Speed in an isolated chat is a comfort feature. Speed inside an agent loop is a capability multiplier, and the difference is the whole point.

## Why latency compounds in a loop

A single completion's latency is annoying at worst. But an agent doesn't do one completion — it does a chain: read context, decide, call a tool, read the result, decide again, maybe back up and retry. Every step pays the latency tax, and the taxes add up. A ten-step task at normal speed is a coffee break. The same task at 14x is a few seconds.

That's not just less waiting. It changes which agent designs are worth building at all. When each model call is cheap in *time*, you can afford loops you'd never tolerate otherwise: generate five candidate approaches and pick the best, re-plan after every tool result, run a verification pass on the agent's own output before showing you anything. All of those multiply your call count, and all of them are gated by how much latency you can stack before the whole thing feels broken. Drop the per-call latency by 14x and patterns that were theoretically-better-but-too-slow become just better.

I've argued before that the harness around the model matters more than the model now. Speed is a harness property in disguise — it sets your budget for how much thinking-out-loud, retrying, and self-checking the loop can do before a human gives up waiting.

## The Cerebras detail is the real signal

The other half of this is *where* the speed comes from. It's not a software trick on the usual GPUs — it's Cerebras, a fundamentally different chip architecture built for exactly this. That's worth noting because it points at where the next round of gains is coming from.

Model quality is converging and prices are falling. The frontier of *differentiation* is moving into inference — specialized silicon, speculative decoding, routing, serving tricks. "Same model, radically different serving characteristics" is going to be a recurring headline, and it means the thing you're choosing when you pick a provider is less the model and more the way they run it. Latency, throughput, and cost-at-speed become first-class selection criteria, not footnotes.

## What I'd actually do with it

Nothing yet — it's a limited preview, and building on preview-tier availability is how you end up rewriting things. But I'd start designing with the assumption that this speed is coming broadly, because it is.

Concretely: if you've been avoiding multi-pass agent patterns because they felt too slow, revisit that assumption soon. The verification-loop and best-of-N designs that are "too expensive in latency" today are the default tomorrow. The teams ready to use cheap-fast inference will have loops designed for it; the teams still doing one-shot calls will be leaving the gains on the table.

If you've already got a workload where per-call latency is the thing stopping you from adding a self-check or a re-plan step, that's the workload to point at fast inference first. Which one is it for you? I'm collecting examples of "I'd add this loop if calls were 10x faster."
