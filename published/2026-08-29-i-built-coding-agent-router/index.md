<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-29-router.png · RECEIPT CARD: assets/2026-08-29-router-receipt.png
- This is a "show your own work" post about github.com/frankchu91/coding-agent-router (Frank's own tool). Facts from the repo README + source (brain.ts: fingerprint lock, escalate-only; prompts/classify.md three tiers; JSONL ledger savings receipts; Anthropic Messages API proxy on port 41414; providers GLM/Kimi/DeepSeek/Qwen/MiniMax).
- Savings example from README: $0.12 spent vs $1.23 frontier-only = 90% saved on that run (6 requests to cheap tier). Honest about variance.
- Ties to published Switchyard + convergence posts. Cross-link both.
- Written to pass aiscan. Re-run node scripts/aiscan.js before publishing.
- No AI-disclosure line (policy).
-->

---
title: "I built a router to cut my Claude Code bill, and prompt caching was the whole problem"
published: false
description: "Cheap model for routine work, frontier model when it's actually hard. Simple idea, one nasty catch: switch models mid-conversation and you invalidate the prompt cache. Here's how I solved it."
tags: ai, agents, typescript, opensource
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-29-i-built-coding-agent-router/cover.png
---

I built a router to cut my Claude Code bill, and it almost made the bill bigger. The culprit was a piece of plumbing nobody mentions when they pitch you on model routing: prompt caching. That one detail is why the obvious version of this idea quietly loses money, and it is what I wish someone had told me before I started.

The idea itself I have argued here for a while. Coding models have converged, most of your agent's work is mechanical, and the smart move is to run cheap by default and escalate to a frontier model only when the task is hard enough to need it. I wrote about NVIDIA productizing that with [Switchyard](https://dev.to/frankchu/nvidia-shipped-the-router-my-benchmark-was-asking-for-so-i-made-it-herd-my-ollama-models-2clf), and about how [my own configuration explains my results](https://dev.to/frankchu/i-went-looking-for-a-reason-to-switch-coding-agents-and-couldnt-find-one-27m1) more than the model does. At some point writing it down stopped being enough, so I built it. It is called [coding-agent-router](https://github.com/frankchu91/coding-agent-router), and it sits in front of Claude Code.

## The obvious version loses money

The naive design is easy to picture. Intercept every request, classify how hard it is, send the easy ones to a cheap model and the hard ones to the frontier. Per request, per step. It feels right, and it backfires, and the reason is prompt caching.

Prompt caching is per-model. A cache entry built against one model is worthless the moment the next request names a different one. Claude Code sends your growing conversation on every step, and normally most of it is a cache hit, so you pay full price once and a fraction after that. Now put a naive router in the middle that picks a model per step: cheap for this tool call, mid for the next, frontier for the one after. Every switch is a cache miss, and the entire conversation history gets re-read at full price on the new model. On a long session you can pay more with the router than without it. The savings are real on the individual cheap call and the cache penalty eats them alive.

That is the trap. Routing and caching pull in opposite directions, and any router that ignores the second one is a savings tool that silently costs you money.

## The fix: decide once, lock, and only ever escalate

The design that actually works treats a conversation as the unit, not a request. When a fresh conversation starts, the router fingerprints it from the system prompt and the first user message, runs a small classifier to score the difficulty, and locks the whole conversation to a tier. Every following step on that conversation follows the lock, so the model stays put and the cache stays warm.

The one exception is the direction that is safe. A locked conversation can escalate up, never down. If a session that started easy turns hard, a human turn can bump it to a higher tier, because spending more to protect your work is the trade you want. The code is blunt about it:

```ts
const next = higher(lock.tier, suggested); // escalate only, never down
```

Downshifts only happen where the cache is already cold anyway: a brand new conversation, or a compact or restart that resets the history. At those boundaries there is no warm cache to protect, so reclassifying is free. Everywhere else, the tier is locked and the cache is safe. That single rule, downshift only at cold boundaries, is the difference between a router that saves money and one that pretends to.

## What the classifier actually does

The classifier is a small, cheap LLM call with one job: score the opening task into cheap, mid, or frontier. Cheap is mechanical work with a clear procedure, like renames, import fixes, formatting, or running a command and reporting output. Mid is routine engineering with some judgment. Frontier is anything with real reasoning or blast radius: debugging an unknown cause, architecture, concurrency, security-sensitive code, or a task whose scope is ambiguous.

Two rules keep it honest. When it is torn between two tiers, it picks the higher one. And it judges the task, not its length, because a one-line request can be the hardest thing you ask all day. The prompt that encodes all of this lives in a versioned file in the repo rather than buried in code, because that prompt is the router's judgment and I would rather argue about it in pull requests than hide it.

## Making it safe to trust

A cost tool that breaks your session is worse than no tool, so the failure modes all point the same way. Uncertain classification routes up. An unparseable request passes through untouched. An upstream failure falls back a tier. The worst case is "you saved nothing on this one," never "your session is broken." I wanted to be able to leave it running without thinking about it, and that only works if every ambiguous case resolves toward safety instead of savings.

The savings are also auditable rather than a vibe. Every request writes to a local ledger with its real cost and the counterfactual of what a frontier-only run would have cost, so the report is arithmetic you can check. A real receipt from one of my sessions:

![coding-agent-router savings report: $0.12 spent vs $1.23 frontier-only, 90% saved on that run](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-29-i-built-coding-agent-router/receipt.png)

That run happened to route six requests to the cheap tier with zero frontier usage, which is realistic for a stretch of mechanical work and not representative of every session. A debugging-heavy afternoon escalates early and saves less. The honest claim is not a fixed percentage, it is that the routine majority of your calls stop being billed at frontier rates.

## Where it lands in the bigger picture

Each tier is just a model, a base URL, and a key, so any Anthropic-compatible endpoint drops in. GLM, Kimi, DeepSeek, Qwen, and MiniMax all expose one, which means "cheap tier" can be an entirely different provider than "frontier tier" if that is where the economics are best that week.

I keep coming back to one theme across everything I write, which is that the model is the commodity and the value is in the harness around it. This is me putting my own code where my posts are. The router does not make any model smarter. It just spends the expensive one only when the expensive one earns it, and it does that without breaking the cache that makes the whole thing affordable in the first place. It is open source, it runs with `npx coding-agent-router claude`, and I would like it to be wrong in ways I have not thought of yet.

If you try it, the thing I most want to hear is where the classifier misjudged a task, because that file is the whole argument and it gets better the more real sessions disagree with it. The repo is [here](https://github.com/frankchu91/coding-agent-router).

There is a lower-tech version of this same idea that skips the proxy entirely: run two agents, a frontier driver and a free open one, and route between them by hand. I wrote that up separately.

{% link https://dev.to/frankchu/the-2026-coding-setup-isnt-one-agent-its-two-a-frontier-driver-and-a-free-open-one-26a %}
