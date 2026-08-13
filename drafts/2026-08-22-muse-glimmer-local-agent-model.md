<!--
REVIEW NOTES (delete before publishing)
- Verified by Claude on 2026-08-12: HF repos exist (meta-models/Muse-Glimmer-30B + GGUF), community quants already up (unsloth/bartowski GGUF, mlx-community 4bit for Macs). Benchmark + speed numbers are Meta's own — phrased as claims.
- OPTIONAL but high-value before publishing: pull the MLX 4-bit on your Mac (~17GB) and run one real agent task; even one paragraph of "here's what happened on my machine" upgrades this post a lot. The text has a marked slot for it.
- Links naturally back to your own local-model wiki post — that reference is real, keep it.
-->

---
title: "Meta shipped a 30B agent model that fits on one GPU, and this time the weights are actually up"
published: false
description: "Muse Glimmer is Apache 2.0, quantized to 17GB, and tuned for local agent loops. What's real, what's claimed, and why the boring details matter."
tags: ai, llm, opensource, machinelearning
---

Part of my own tooling runs on a free local model — I wrote about that setup [a few weeks ago](https://dev.to/frankchu/making-an-ai-maintained-wiki-run-on-a-free-local-model-what-actually-worked-3n7n) — and the honest summary is that the model has always been the weakest part. Local models are fine at single constrained completions. Ask one to sit inside an agent loop, calling tools and recovering from its own mistakes, and things get rough.

So Meta's release on Monday got my attention. Muse Glimmer is a 30B multimodal model distilled from Muse Spark, tuned specifically for what Meta calls always-on local agent workflows, and licensed Apache 2.0. Not "weights coming soon," either — I checked before writing this. The repos are up on Hugging Face under `meta-models`, and the community had GGUF and MLX 4-bit conversions posted within about two days, which is usually a decent sign of real interest.

After a couple of weeks where the biggest open-weights story was a 2.4-trillion-parameter model most of us could never run, a 30B built to live on one consumer GPU feels like it was aimed at people like me.

## The quantization is the actual product

At full precision the model needs more than 55GB of memory, which rules out every consumer card. What Meta shipped alongside it is the interesting part: two official 4-bit builds — one targeting 32GB of VRAM with a claimed 0.2% quality loss, and a 17GB build that fits a 24GB card at a claimed 1.0% loss.

Those degradation numbers are Meta's own, and quantization claims are exactly the kind of thing I'd test before trusting; a model can hold its benchmark scores through quantization and still get subtly worse at the long-horizon stuff agents need. But publishing official quants at all, instead of leaving it to the community, tells you who this release is for.

The other piece is a speculative-decoding drafter called DFlash. Meta's numbers: an RTX 5090 goes from about 75 to 233 tokens per second with it, and an M4 Max from 24 to 38. Speed matters more than usual here, because an agent loop multiplies every latency by the number of steps. A model that's tolerable in a chat window can be unusable inside a ten-step tool loop, and 30-something tokens per second on a Mac is right around where that line sits, in my experience.

<!-- PERSONAL TAKE: if you ran the MLX build on your Mac, put what actually happened here — download size, tokens/sec you saw, one task it handled or fumbled. This paragraph is the post's centerpiece if you have it. -->

## The claims I'm not repeating as facts

Meta reports leading scores for its size class on agent-flavored benchmarks — MCP Atlas 75.5, SWE-Bench Pro 51.2, Gaia2 43.3, and a striking 94.7 on AIME 2026. All self-reported, all launch-week. I've written before about [what I check before believing open-weights benchmarks](https://dev.to/frankchu/qwen38-max-says-it-beats-gpt-56-and-fable-5-at-computer-use-heres-my-checklist-before-i-believe-48h0), and everything there applies. The independent numbers will show up within a couple of weeks; the interesting question is narrower than a leaderboard anyway.

The question that matters to me: is this the first open model where the *local agent loop* — not chat, not one-shot code generation — is actually the design target? The pieces suggest Meta thinks so. Official quants sized to real cards, a drafter tuned for loop latency, multimodal input so it can look at screenshots. Somebody at Meta drew the same conclusion a lot of us have: the next place agents run is on the machine you own.

## Worth saying plainly

"Always-on local agent" is doing quiet work in that pitch. A model resident in memory, watching and acting all day, is a space heater and a security surface as much as it is a convenience — an agent with local file access doesn't stop being a risk just because inference happens on your own GPU. And Apache 2.0 on the weights doesn't tell you anything about what it was trained on; it tells you what you're allowed to do with the result.

Still. A year ago the local-model story was "impressive for what it is." This release reads like the first one built for the job I actually want done: a competent agent on my own hardware, no meter running, no tokens leaving the house. Whether it delivers that is a download and an evening away, which is exactly the kind of claim I like — cheap to check.

If you get it running before I finish my own testing, tell me what you saw. Especially the failures.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
