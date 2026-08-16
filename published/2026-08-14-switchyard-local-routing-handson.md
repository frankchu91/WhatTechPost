<!--
REVIEW NOTES (delete before publishing)
- ASSETS live in drafts-assets/ (local, gitignored). On publish: move markdown to published/, move this post's PNGs to assets/, push — then the raw URLs below resolve and paste/API needs no image steps.
- Every number and error in this post happened on this machine today (2026-08-13); raw notes in research/2026-08-13-switchyard-handson.md.
- Publish after the Qwen follow-up. Suggested order: today Qwen, tomorrow this, Muse Glimmer bench after (or swap the last two).
- The three install bugs may get fixed quickly — if the post goes out more than a few days late, re-verify `uv tool install "nemo-switchyard[cli]"` still fails without the extra --with packages.
-->

---
title: "NVIDIA shipped the router my benchmark was asking for, so I made it herd my ollama models"
published: false
description: "Switchyard's escalation router in front of llama3.2:3b and qwen3:14b: three packaging bugs, an undocumented YAML schema, and then it genuinely worked."
tags: ai, llm, opensource, python
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-14-switchyard.png
---

Earlier this week I benchmarked three local models on agent tasks and landed on a rule: keep the small model in the loop for the routine work, and escalate to a big one only when a step actually needs to think. The obvious follow-up question was who does the escalating. My honest answer was "some if-statements I haven't written yet."

Two days later NVIDIA open-sourced [NeMo Switchyard](https://github.com/NVIDIA-NeMo/Switchyard), a Rust proxy that routes LLM traffic across models — including a judge-latched escalation router that starts every conversation on a weak model and promotes it to a strong one when an LLM judge decides the conversation deserves it. That's not approximately my conclusion; it's exactly my conclusion, productized. So I spent the afternoon wiring it up to the ollama models already on my Mac.

It worked, eventually, and the eventually is half the story.

## Three bugs before hello world

The quick start says to install with `uv tool install --python 3.10 "nemo-switchyard[cli]"`. That command fails: the package requires Python 3.12 or newer, and the docs pin 3.10. Drop the flag and it installs.

Then `switchyard serve` crashed with `No module named 'yaml'`. The CLI extra doesn't declare pyyaml. Adding it got me to the next crash — `No module named 'uvicorn'`. The incantation that finally worked:

```bash
uv tool install --force --with pyyaml --with uvicorn --with fastapi "nemo-switchyard[cli]"
```

This is launch-week open source in its natural state, and I don't say that meanly — the Rust core is clearly where the engineering went, and the Python packaging will catch up. But if you try it this week, now you know.

## The undocumented part

The docs describe a TOML config for the Rust server path. The Python CLI's `serve` command wants something else: a YAML "route bundle" with `--routing-profiles`, and I couldn't find that format documented anywhere. I ended up reading the installed package's `route_bundle.py` to learn the shape. Five route types are registered; the one I wanted was `escalation_router`, which takes `weak`, `strong`, and `judge` targets. This got a proxy serving on port 4000:

```yaml
routes:
  local:
    type: escalation_router
    weak:   {model: llama3.2:3b, base_url: http://localhost:11434/v1, api_key: ollama}
    strong: {model: qwen3:14b,   base_url: http://localhost:11434/v1, api_key: ollama}
    judge:  {model: llama3.2:3b, base_url: http://localhost:11434/v1, api_key: ollama}
    fallback_target_on_evict: weak
```

Note the judge is the 3B. A small model deciding when a conversation is too hard for small models — we'll see how that went.

## Does the proxy cost anything?

The route shows up at `/v1/models` as an OpenAI-compatible model called `local`, so any client that speaks the OpenAI API can use it unmodified. First request through the proxy took 3.8 seconds against 0.2 direct — one-time warmup. After that, warm proxy calls were 0.18–0.30s against 0.16–0.18s direct. Call it under a tenth of a second of overhead: for local routing, effectively free.

Simple questions came back from `llama3.2:3b` — the response's `model` field tells you who actually answered, which makes the whole thing pleasantly inspectable.

## Making it escalate

Then I tried to trigger the interesting part. A four-turn conversation of moderate difficulty stayed on the 3B throughout — the judge only starts evaluating at turn three by default, and needs two consecutive escalate verdicts, so early promotion is deliberately hard. (Those thresholds exist in the config model but aren't exposed in the YAML, so you live with the defaults for now.)

So I picked a fight: a seven-turn conversation that starts at "implement a lock-free MPMC queue" and ratchets through hazard pointers, linearizability proofs, and a TLA+ spec, with me rejecting every answer as insufficiently rigorous.

```
turn 1: model=llama3.2:3b  wall=1.9s
...
turn 6: model=llama3.2:3b  wall=3.8s
turn 7: model=qwen3:14b    wall=21.0s
```

![Wall time per turn: turns 1-6 answer in 1.8-3.8s on the 3B, turn 7 jumps to 21s on the escalated 14B](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-14-switchyard-chart.png)

Turn seven, the judge folded and promoted the session to the 14B — a one-way latch, so the conversation stays on the strong model from there. The proxy's `/v1/stats` endpoint shows token accounting for both models. Everything ran on my laptop; nothing left the house; the total cost of all of this was electricity.

Whether turn seven was the *right* moment is a fair question — I'd have escalated around turn three, when the answers first got hand-wavy. A 3B judging what exceeds a 3B is grading its own homework, and it grades generously. If the judge tuning gets exposed in the YAML, that's the first knob I'd turn.

## Where I landed

Setup was rougher than the announcement suggests, the YAML is undocumented, and the judge is conservative to a fault. And still — this is the first tool I've used that treats "small model by default, big model on demand" as infrastructure instead of a blog-post aspiration. The pattern I was hand-rolling on Tuesday had a maintained Rust implementation by Friday. That's the part worth knowing about, whatever router you end up using.

If you know a cleaner way to expose the judge thresholds — or you've watched a bigger judge earn its keep — the comments are open.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
