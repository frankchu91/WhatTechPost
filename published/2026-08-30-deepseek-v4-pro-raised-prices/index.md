<!--
REVIEW NOTES (delete before publishing)
- COVER: cover.png · CHART: price-chart.png (peak vs off-peak vs cached)
- Facts (research/2026-08-30-topic-scan.md): DeepSeek V4-Pro GA (build 0813, Aug 12-13): 1.6T total / 49B active, 1M context, up to 384K output, agent-focused, new low/high/max "thinking effort" selector. PRICING (raised Aug 17): Pro ~$1.32 in / $3.96 out at PEAK (up from ~flat $0.87 out); off-peak = half price; cache hits ~97% discount. Flash $0.44/$1.32.
- NO META. aiscan PASS required.
- No AI-disclosure line (policy).
-->

---
title: "DeepSeek raised its prices in the middle of a price war. That's the part worth noticing"
published: false
description: "V4-Pro left preview with a low/high/max effort dial and, unusually, a price increase — while everyone else is cutting. The pricing structure says more than the benchmarks do."
tags: ai, llm, agents, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-30-deepseek-v4-pro-raised-prices/cover.png
---

DeepSeek raised its prices. That is the one thing almost nobody in this industry has done this year, and it is why I stopped scrolling. For months everyone has been cutting, an 80% slash here, a halved intro rate there, everyone racing the cost of a token toward zero. And then DeepSeek, of all companies, the one whose whole reputation is being shockingly cheap, put its flagship's output price up. Signals that run against the trend are usually the ones worth reading.

The occasion was V4-Pro leaving preview this month, a 1.6-trillion-parameter flagship, agent-focused, with a million-token context and a new low, high, and max "thinking effort" selector. All of that is interesting. But I have spent [a run of posts tracking this price war in actual numbers](https://dev.to/frankchu/the-ai-api-price-war-in-actual-numbers-what-id-run-my-agents-on-this-month-2nno), and a price increase is the first move in it that genuinely surprised me.

## The effort dial is the feature, and it's a familiar one

Start with the capability, because it lines up with something I keep seeing. V4-Pro's headline feature is a thinking-effort selector: low, high, or max. You choose how hard the model reasons per request, trading speed for depth on purpose.

That is the same idea showing up everywhere now. It is the [escalation router I built](https://dev.to/frankchu/i-built-a-router-to-cut-my-claude-code-bill-and-prompt-caching-was-the-whole-problem-3ifl) to cut my own bill, the per-subagent model control in coding agents, the general move toward spending expensive reasoning only where it earns its keep, except here it is baked into the model as a dial you turn. The industry has converged on a simple truth: most requests do not need maximum reasoning, and paying for it anyway is waste. A first-class effort control is that truth turned into an API parameter, and it is quietly one of the most practical features a model can ship.

## Now the pricing, which is where it gets strange

Here is the structure DeepSeek moved to. Peak-hours pricing went up, with V4-Pro output landing around $3.96 per million tokens, a real jump from the flat sub-dollar rate people got used to. But off-peak hours run at half price, and cache hits are discounted by roughly 97%.

![DeepSeek V4-Pro output price per 1M tokens: about $3.96 at peak hours versus $1.98 off-peak, on top of a roughly 97% discount for cached tokens](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-30-deepseek-v4-pro-raised-prices/price-chart.png)

Read that as a whole and it is not really a price increase. It is a price restructuring that looks like an increase if you only glance at the peak number. DeepSeek is doing what electricity utilities and airlines do: charge more when demand is high, reward you heavily for using the system when it is idle or for reusing what is already cached. The 97% cache discount especially tells you where they want your traffic, because agent workloads re-read the same context constantly, and a near-total discount on cached tokens is a direct invitation to build agents that lean on caching.

So the "price increase" is really a nudge. Pay a premium for peak, on-demand, uncached reasoning, or restructure your usage around off-peak and cache and pay less than before. It is the pricing of a company that has enough demand to start shaping it rather than just chasing the bottom.

## What a price increase signals in a race to zero

This is the part I find genuinely worth sitting with. When everyone is cutting and one serious player raises peak prices, a few things could be true, and they are all interesting.

It could mean demand is outrunning capacity, so peak pricing is a way to ration compute rather than a grab for margin. It could mean DeepSeek thinks V4-Pro is good enough that people will pay, which is a confidence signal about the model. And it could mean the race to zero has a floor, that serving a 1.6-trillion-parameter model at genuinely high quality costs real money, and the pure price-dumping phase is giving way to pricing that reflects cost and demand. Probably it is some of all three.

For builders the practical read is clear. Cheap flat-rate inference was a moment, not a permanent condition, and the smarter providers are moving to structured pricing where when and how you call matters as much as how much. Design your agents for it. Lean on caching hard, because a 97% cache discount is the single biggest lever on your bill. Run batch and low-stakes work off-peak if your provider prices that way. And treat the effort dial as a cost control, not just a quality knob, because low effort on the routine majority of calls is where the savings actually live.

The benchmarks will get argued over like they always do. The pricing move is the more durable signal, and it says the era of racing the token price to zero is maturing into something that looks a lot more like how every other utility eventually prices a scarce resource.

If you have restructured an agent workload around off-peak or cache pricing and watched the bill move, I would like to hear the numbers, because that is the real test of whether this structure helps builders or just reshapes the bill.
