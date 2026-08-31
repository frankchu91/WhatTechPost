<!--
REVIEW NOTES (delete before publishing)
- All prices from vendor announcements / coverage as of 2026-08-07 (sources in research/2026-08-07-topic-scan.md). RE-CHECK current pricing pages the day you publish — this war moves weekly.
- The monthly cost table is arithmetic on the stated workload; math verified.
- YOUR TAKE SLOT: [PERSONAL TAKE] — which model you actually route to in your product and why.
- Timing: publish before Sep 1 (Sonnet 5 intro pricing deadline is the hook).
-->

---
title: "The AI API price war, in actual numbers: what I'd run my agents on this month"
published: false
description: "GPT-5.6 Luna dropped 80%, Sonnet 5's intro price dies Sep 1. A real cost table for a real agent workload, and how I'd route between tiers."
tags: ai, llm, programming, productivity
---

On July 30, OpenAI cut the price of GPT-5.6 Luna by 80%. Not a typo: $1.00/$6.00 per million tokens became **$0.20/$1.20**. Terra dropped 20% to $2/$12. The flagship Sol didn't move.

Meanwhile Anthropic's Sonnet 5 is sitting at an introductory $2/$10 that reverts to $3/$15 on **September 1** — three weeks from now. And Alibaba priced Qwen3.8-Max at $2/$6 with $0.25 cached input.

Price is now a strategy weapon, and if you run agents, your bill is suddenly negotiable. Let's do the arithmetic nobody's announcement includes.

## The board as of this week

| Model | Input /1M | Output /1M | Notes |
|---|---|---|---|
| GPT-5.6 Luna | $0.20 | $1.20 | was $1/$6 until Jul 30 |
| GPT-5.6 Terra | $2.00 | $12.00 | was $2.50/$15 |
| GPT-5.6 Sol | $5.00 | $30.00 | unchanged |
| Claude Sonnet 5 | $2.00 | $10.00 | **$3/$15 after Sep 1** |
| Claude Opus 5 | $5.00 | $25.00 | |
| Qwen3.8-Max | $2.00 | $6.00 | $0.25 cached input |

## What that means for a real workload

Take a workload I think is representative of a solo builder running a coding/ops agent daily: **3M input + 300K output tokens per day** (agents are input-heavy — context re-reads dominate). Over 30 days that's 90M in / 9M out:

| Model | Monthly cost |
|---|---|
| GPT-5.6 Luna | **$28.80** |
| Qwen3.8-Max | $234 |
| Sonnet 5 (intro) | $270 |
| Terra | $288 |
| Sonnet 5 (from Sep 1) | $405 |
| Opus 5 | $675 |
| Sol | $720 |

Two things jump out of that table.

First, the spread between cheapest and priciest is now **25x** for the same token volume. A year ago the tiers were maybe 5x apart. The vendors are telling you, loudly, that most agent traffic doesn't need a flagship.

Second, caching changes the ranking. Qwen's $0.25 cached input means that same workload at a realistic 70% cache-hit rate lands around **$124/month** — agents re-read the same context constantly, so cached-input pricing is worth more to agent builders than headline price. Check your provider's caching discount before comparing base rates; it's where the real money is.

## How I'd actually route

The mistake is picking one model. The move is routing by task risk:

- **High-volume, low-stakes** (classification, extraction, summarizing logs, first-pass triage): Luna at $0.20/$1.20 is close to free. If you're doing this on a flagship, you're donating money.
- **The agent's main loop** (code edits, multi-step tool use): Sonnet 5 or Terra tier. This is where quality drops actually cost you time.
- **Escalation only** (gnarly debugging, architecture decisions, final review): Sol or Opus 5, invoked by the cheaper model when it's stuck, not by default.

## The catch nobody prints

An 80% price cut on last quarter's mid-tier is also a signal about where that model sits in the lineup now. Vendors cut prices on tiers they've already beaten internally. You're not getting a discount on the frontier; you're getting the previous frontier at clearance. That's still a great deal — just don't confuse it with generosity.

And mind the reversion dates. Sonnet 5's intro pricing expiring Sep 1 is a 50% jump on both sides of the meter. If your margins depend on intro pricing, you don't have a margin — you have a countdown.

What's your actual monthly spend and split? Genuinely curious what routing setups people have landed on — drop your numbers in the comments.

Update: the race to zero I describe here did not hold. DeepSeek went the other way and raised its prices, which turns out to be the more interesting move.

{% link https://dev.to/frankchu/deepseek-raised-its-prices-in-the-middle-of-a-price-war-thats-the-part-worth-noticing-2o49 %}

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
