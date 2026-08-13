<!--
REVIEW NOTES (delete before publishing)
- All numbers in this post are from a real run on this machine, 2026-08-12: script scripts/bench_local_agents.py, raw results research/data/bench-2026-08-12.jsonl. Repo link in the post — make the repo public before publishing, or remove the link.
- think:false finding verified with two runs (cold 231s reload-included; warm 11s/60tok). Wording in the post matches what we saw.
- n=5 per test is honest-but-small; the post says so explicitly. Don't let edits remove the limitations section.
-->

---
title: "Meta says its new 30B is built for local agents. I benchmarked it against the two models already on my Mac"
published: false
description: "Muse Glimmer vs qwen3:14b vs llama3.2:3b on the tasks an agent loop actually does all day — real numbers from an M2 Pro, script included."
tags: ai, llm, opensource, machinelearning
---

Meta released Muse Glimmer on Monday: a 30B model, Apache 2.0, official 4-bit quants, pitched specifically for always-on local agent workflows. I'd already pulled it the day it landed, and it had been sitting next to two other models in my ollama list — qwen3:14b and llama3.2:3b — which is a natural experiment waiting to happen.

Because the question that actually matters to me isn't "is the 30B smarter." Of course it's smarter. The question is whether it earns its seat in a local agent *loop*, where every call's latency gets multiplied by the number of steps. So instead of reading more launch coverage, I wrote a small benchmark and ran all three models through the work my agent tooling actually does all day.

## The setup

MacBook Pro, M2 Pro, 32GB RAM. ollama 0.32.7. Muse Glimmer is the community MLX build (21GB on disk, runs 100% GPU) — one honest caveat up front: this is *not* Meta's official stack, and it doesn't include DFlash, their speculative-decoding drafter that produced the impressive launch-day speed numbers. More on that below.

Three tests, chosen because they're what agent loops are made of:

1. **Context re-read speed** — a ~1,000-token prompt, measuring prompt-processing and generation rates. Agents re-read context constantly; prompt speed usually matters more than generation speed.
2. **Constrained JSON** — extract fields into an exact four-key schema, five runs each, temperature 0. Checked for valid JSON and exact schema conformance. This is the single most common thing my local tooling asks a model to do.
3. **Tool calling** — a two-step "use the tool, answer the question" task, three runs each.

The script and raw results are [in the repo](https://github.com/frankchu91/WhatTechPost) if you want to rerun this on your own hardware.

## The numbers

| model | prompt tok/s | gen tok/s | JSON schema | sec/call | thinking tok/call | tools |
|---|---|---|---|---|---|---|
| llama3.2:3b | 702.9 | 56.7 | 5/5 | 0.6 | 0 | 3/3 |
| qwen3:14b | 161.8 | 14.6 | 5/5 | 16.1 | ~227 | 3/3 |
| muse-glimmer:30b | 56.7 | 7.1 | 5/5 | 33.4 | ~284 | 3/3 |

Two things surprised me, and neither was the one I expected to write about.

## Everyone passed. That's the story.

I assumed the correctness columns would separate the models. They didn't — every model went five-for-five on schema conformance and three-for-three on tool selection, including the 3B. For the bread-and-butter tasks of an agent loop, correctness at this difficulty is simply solved, all the way down to two gigabytes of weights.

Which turns the comparison into pure economics. The same JSON extraction costs 0.6 seconds on the 3B and 33.4 seconds on Muse Glimmer — a 56x difference for an identical, equally-correct result. Chain five of those calls and it's the difference between a three-second loop and a three-minute one.

Where does the time go? Partly raw size, but mostly deliberation. Muse Glimmer is a thinking model, and it spent roughly 284 tokens per call reasoning about a task that does not need reasoning — at one point the thinking trace literally restated my prompt to itself twice before answering. qwen3:14b does the same thing, just less of it. The 3B doesn't think at all, in the best possible sense.

I did try turning it off. ollama accepts `think: false` for this model, and the thinking trace obediently disappears — but the cost mostly doesn't. With a 60-token budget I got an empty response back: the model was still deliberating, just invisibly, and burned the whole budget before reaching its answer. Give it 120 tokens and the correct JSON shows up, at roughly half the full-thinking latency but still around 25x slower than the 3B. As far as I can tell the deliberation is baked into the weights; the flag controls whether you get to watch.

## About Meta's speed numbers

Meta's launch material reports around 38 tok/s on an M4 Max with DFlash. I measured 7.1 tok/s generating on an M2 Pro. Some of that gap is my older chip, but most of it is that the DFlash drafter simply isn't in the community builds yet — the launch-day numbers describe Meta's stack, not the one you get from `ollama pull` today. If the drafter lands in mainstream runtimes, the arithmetic above changes meaningfully. Until it does, plan around the numbers your own runtime gives you.

## What this benchmark can't tell you

Five runs per test, one schema, one trivial tool task — this measures the floor an agent loop stands on, not the ceiling. The tasks where a 30B should justify itself (multi-step planning, recovering from a failed approach, reading an actual screenshot) aren't in here, and on those I'd still expect Muse Glimmer to beat the smaller models by a lot. I'll test that separately once I have a fair harness for it.

## Where I landed

The conclusion I keep coming back to: route your local models the way you'd route API models. The loop's high-frequency work — extraction, formatting, classification, simple tool dispatch — belongs to the smallest model that passes your checks, and on my machine that's a 3B running at 700 tokens per second of prompt processing. The 30B's job is to be the escalation tier: the model you call when a step actually needs to think, with the tokens never leaving the house.

That's a real niche, and Muse Glimmer, Apache-licensed and genuinely downloadable today, is a credible occupant of it. It's just not the model I'd put *inside* the loop — and "built for always-on local agents" quietly implies it should be.

If you rerun the script on an M4 or a 24GB CUDA card, I'd like to see your table.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
