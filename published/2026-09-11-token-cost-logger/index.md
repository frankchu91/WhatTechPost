<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 2 (9/11), post 2/3. FORMAT: hands-on tool. First-hand (the router keeps a JSONL savings ledger; this is that idea as a standalone 30-line wrapper). Real code.
- Facts: response.usage has input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens (verified vs Claude API usage fields). Prices illustrative — tell readers to use current provider prices. Cache reads ~0.1x input.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "A 30-line wrapper that tells you what every LLM call actually costs"
published: false
description: "You don't find out what your agent spends until the invoice lands. A thin wrapper reads the usage each response already returns, prices it, and logs a line. Now the bill is visible while you build."
tags: ai, llm, python, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-11-token-cost-logger/cover.png
---

Most people building with LLMs do not know what a given call costs until the monthly invoice shows up, and by then it is a single scary number with no breakdown. The fix is small. Every response already tells you how many tokens it used. Wrap the client once, price that usage against a table, and log a line per call. Now you can see the bill accumulate while you build, and you can find the one route that is eating it.

## The usage is already in the response

You do not need a proxy or a dashboard to start. The response object carries a `usage` block with the token counts, and on the Claude API that is `input_tokens`, `output_tokens`, and separately `cache_read_input_tokens` and `cache_creation_input_tokens` for anything that hit or wrote the prompt cache. The only thing you add is a price table and a multiply.

```python
import json, time

# $ per 1M tokens — use your provider's CURRENT prices.
PRICES = {
    "claude-opus-5":   {"in": 5.0,  "out": 25.0},
    "claude-sonnet-5": {"in": 2.0,  "out": 10.0},
}

def cost_of(model, usage):
    p = PRICES[model]
    cached = getattr(usage, "cache_read_input_tokens", 0) or 0
    fresh_in = usage.input_tokens - cached
    # cache reads bill around a tenth of normal input
    return (fresh_in * p["in"] + cached * p["in"] * 0.1
            + usage.output_tokens * p["out"]) / 1_000_000

def logged_call(client, label, **kwargs):
    resp = client.messages.create(**kwargs)
    c = cost_of(kwargs["model"], resp.usage)
    line = {"t": time.time(), "label": label, "model": kwargs["model"],
            "in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
            "usd": round(c, 6)}
    with open("llm_cost.jsonl", "a") as f:
        f.write(json.dumps(line) + "\n")
    print(f"[{label}] ${c:.4f}  ({resp.usage.output_tokens} out)")
    return resp
```

That is the whole thing. Call `logged_call(client, "summarize", model=..., messages=...)` instead of the raw create, and every call drops a priced line into a JSONL file.

## Why a label and a JSONL file

The label is the part that turns a number into an answer. Tag each call with the feature or route it belongs to, summarize, classify, the main agent loop, and later you can group the JSONL by label and see that one path is eighty percent of your spend. That is the thing the invoice can never tell you, and it is usually where the savings are hiding. JSONL because it is append-only, trivially greppable, and you can load a day of it into a notebook without any infrastructure.

```python
# which routes cost the most today?
import collections, json
totals = collections.Counter()
for line in open("llm_cost.jsonl"):
    r = json.loads(line); totals[r["label"]] += r["usd"]
for label, usd in totals.most_common():
    print(f"{label:20} ${usd:.2f}")
```

## Two things the naive version gets wrong

Count cached tokens separately. If you price every input token at the full rate, you will badly overstate cost on any app that uses prompt caching, because cache reads are roughly a tenth of the price. The wrapper above pulls `cache_read_input_tokens` out and prices it low, which is the difference between a useful number and a misleading one.

Watch output, not input. Output tokens are several times more expensive than input on most models, so a call that returns a long answer usually costs more than one that reads a long prompt. When you go looking for savings, the verbose responses are the first place to look, not the big prompts.

This is the kind of tool that pays for itself the first afternoon. The bill stops being a surprise, the expensive route stops being a mystery, and you made both true with thirty lines and the usage numbers the API was already handing you.

If you track your own spend some other way, I want to see it, because the people who actually measure this tend to have found something the rest of us are guessing at.
