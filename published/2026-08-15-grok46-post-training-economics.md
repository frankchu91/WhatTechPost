<!--
REVIEW NOTES (delete before publishing)
- ASSETS live in drafts-assets/ (local, gitignored). On publish: move markdown to published/, move this post's PNGs to assets/, push — then the raw URLs below resolve and paste/API needs no image steps.
- Facts verified via Artificial Analysis / VentureBeat / xAI announcement coverage (2026-08-13 search). Numbers: AA Index 61 (tied GPT-5.6 Sol Max), Terminal-Bench v3 26% vs 15.7% for 4.5, 500K context, $2/$6 (doubles past 200K prompt tokens), fast variant 2x price.
- Re-check Artificial Analysis leaderboard the day of publishing — positions move.
-->

---
title: "Grok 4.6 is the same model wearing a better education, and that's the story"
published: false
description: "No bigger base model — just post-training. Five points on the intelligence index at flat $2/$6 pricing. What that says about where capability comes from now."
tags: ai, llm, machinelearning, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-15-grok46.png
---

SpaceXAI released Grok 4.6 this week, and the detail I keep returning to isn't a benchmark. It's what they *didn't* do: there's no larger base model underneath. Grok 4.6 is Grok 4.5 with a longer supplemental training run, regenerated fine-tuning trajectories, and reinforcement learning in agentic environments. Same foundation, better education.

The education bought a lot. Five points on the Artificial Analysis Intelligence Index — now at 61, tied with GPT-5.6 Sol Max and past Kimi K3. Terminal-Bench v3 went from 15.7% to 26%, nearly doubled. And the pricing didn't move: $2/$6 per million tokens, roughly 60% below Sol's rates, with the usual fine print (rates double past 200K prompt tokens, and a "fast" variant costs twice as much).

![Price per 1M tokens: Grok 4.6 at $2/$6 undercuts Sonnet 5 ($3/$15) and GPT-5.6 Sol ($5/$30)](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-15-grok46-chart.png)

## Post-training is the new scaling

For years the roadmap to a better model was a bigger model, and the bigger model cost more to run, so capability and price climbed together. A post-training upgrade breaks that link: inference costs the same as before, because it *is* the model from before. That's how you get a five-point jump at flat pricing — the improvement lives in the weights' arrangement, not their count.

You can see the same move across the industry if you look for it. The gains this year keep coming from RL in agentic environments, from better trajectory data, from longer refinement runs — not from parameter counts, which nobody even brags about anymore. (Alibaba's 2.4T disclosure last week was notable mostly because disclosure has become rare.) The frontier is quietly becoming a competition in curriculum design.

For those of us buying tokens, this is straightforwardly good: capability per dollar keeps improving without the migration pain of a new model family. Grok 4.6 dropped into Cursor and the API the day it launched — same interface, same price, better answers, plus a new `xhigh` reasoning-effort tier if you want to spend more deliberately.

## The claim worth watching

The launch's emphasis is long-running agents — 500K context and RL specifically in agentic environments. That Terminal-Bench doubling is the supporting evidence, and it's the number I trust least and want verified most, for a familiar reason: agentic benchmarks are exquisitely sensitive to harness details, and vendor-run agentic benchmarks doubly so.

But notice the shape of the bet. xAI didn't spend its training budget on trivia or math this cycle; it spent on tool use, recovery, and multi-step work. So did Meta with Muse Glimmer's agent tuning. So did Alibaba with Qwen's computer-use scores. Every lab is now training for the loop, because the loop is where the tokens get bought. Models are increasingly *shaped* by what agents need — which means the benchmarks that matter to you are the agentic ones, and those are exactly the ones hardest to trust from a press release.

## Where I land

Two practical takeaways. First, if you're already routing between model tiers, Grok 4.6 at $2/$6 lands in the same slot as Sonnet 5 and Qwen3.8-Max — the "capable mid-tier" is now genuinely crowded, and the mid-tier is where most agent traffic should run anyway. The price war I wrote about last week keeps escalating from new directions.

Second, watch the pattern more than the product. When frontier-tier capability arrives via post-training at flat prices twice in a month, the lesson is that today's "good enough" tier will be noticeably better in a quarter without you changing a line of code. Architect for model swap-ability — same conclusion as always, arriving from yet another angle.

No open weights here, to be clear — API, Cursor, OpenRouter, and friends only. If you've pushed it on real long-horizon tasks already, the comments are open; I'd particularly like to hear whether the 500K context stays coherent at depth or just fits.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
