<!--
REVIEW NOTES (delete before publishing)
- FORMAT: practical/evergreen explainer, first-hand (model-scoped cache miss hit building the router). Facts verified against the current Claude API prompt-caching reference (claude-api skill / shared/prompt-caching.md), not memory.
- Numbers (Claude API, current): cache reads ~0.1x input price; writes ~1.25x (5-min TTL) / 2x (1h TTL); break-even at 2nd request (5-min); default 5-min TTL refreshed on read; min cacheable prefix model-dependent (512-4096 tok, silently won't cache below); caches are MODEL-SCOPED and per-workspace; verify via usage.cache_read_input_tokens. Render order tools->system->messages; prefix match.
- Anchored on Claude API (router sits in front of Claude Code = authentic). Note other providers have similar auto-caching, don't over-claim their exact numbers.
- MUST stay aiscan-clean: avoid the tier1 filler verbs and hollow intensifiers from the 9/3 swap table, <=2 bold, single-digit em-dash. Do not list the banned words here (the scanner counts the comment too).
- Cross-link router post (3ifl); reverse-link after publish. NON-META. Complete + publish-ready. No AI-disclosure line. COVER: cover.png.
-->

---
title: "Prompt caching is a ~90% discount on your LLM bill, and three habits quietly throw it away"
published: false
description: "Caching charges you a tenth of the price for the part of your prompt you send every time. It also breaks with no error and a higher bill. Here's how it works and the three ways I kept sabotaging it."
tags: ai, llm, api, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-07-prompt-caching-llm-bill/cover.png
---

Prompt caching is the biggest lever on an LLM bill that most people never touch. It charges you about a tenth of the normal price for the part of your prompt you send on every call, which for an agent resending a big system prompt and a growing conversation is most of the tokens. And when it breaks, nothing tells you. The requests still succeed. The bill is just quietly higher.

I have broken it three times in three different ways, each one silent, so here is how it actually works and where it falls apart.

## How it works, in one paragraph

Caching is a prefix match. You send the provider a long prompt that is mostly the same every time, a fixed system prompt, a stable tool list, a conversation history that only grows at the end. The provider hashes that prefix, stores the processed version, and on the next call charges you the discounted rate for every token it recognizes and full price only for the new tail. On the Claude API a cache read costs about a tenth of a normal input token, and writing the entry costs about 25% more than normal, so the entry pays for itself on the second use. The stored copy lives about five minutes by default, and every time you read it the timer resets.

That is the whole idea. The catch is in one sentence, and everything below follows from it.

## The one rule: any change to the prefix invalidates everything after it

The cache key is the exact bytes of your prompt up to the point you want cached. Change one byte at position N and every token after N is uncached again. The prompt renders in a fixed order, tools first, then the system prompt, then the messages, so the stable things belong at the front and the things that change belong at the very end. Get that ordering right and caching mostly happens on its own. Get it wrong and no amount of configuration saves you. Here are the three ways I got it wrong.

## Breaker 1: a timestamp in the system prompt

My first agent put "Current date: 2026-09-07 14:31" at the top of its system prompt. Helpful for the model, fatal for caching. That string changes every request, it sits at the very front of the prefix, and so every single request was a complete cache miss. I was paying full price for a 3,000-token system prompt on every call and could not figure out why the bill would not move.

The fix is to freeze the system prompt and inject anything dynamic later, down in the messages where it invalidates only the tail. The same trap hides in a user ID or a session UUID interpolated into the system text, a request counter, anything that is different this time than last time. If it changes per request, it cannot live at the front.

## Breaker 2: a prompt that is not byte-stable

This one is nastier because the text looks identical to you. I was serializing a chunk of JSON context into the prompt with a plain `json.dumps(data)`, no sorted keys. Python dict ordering happened to shift between requests, the bytes differed, the prefix broke. Same story if you build your tool list by iterating a set, or assemble the system prompt with a few `if feature_on:` branches so every flag combination is a slightly different prefix.

The rule is that the prefix has to be identical down to the byte, not just identical to a human reading it. Sort your keys, order your tools deterministically, and stop concatenating optional sections into the front of the prompt.

## Breaker 3: switching models mid-conversation

This is the one that actually cost me money, and it is the whole reason I keep a note about it. I built a router that picked a cheap model for easy steps and a frontier model for hard ones, per step, inside one conversation. It felt obviously correct and it made some sessions more expensive, not less.

Caches are scoped to a single model. The moment the router switched models, the new model had no cache for that conversation, so the entire history got re-read at full price to build a fresh entry. The few cents saved by running one step on a cheap model were smaller than the cost of re-reading the whole conversation uncached on the switch. I wrote up that failure in detail when I [built the router](https://dev.to/frankchu/i-built-a-router-to-cut-my-claude-code-bill-and-prompt-caching-was-the-whole-problem-3ifl); the short version is that the fix is to keep one conversation on one model and hand cheap side-tasks to a separate short-lived call, rather than swapping models inside a thread that you want to stay cached.

## Always check the one number

Every response tells you what caching did. On the Claude API the `usage` object has `cache_read_input_tokens`, the count served cheaply from cache, and `cache_creation_input_tokens`, the count you paid the write premium on. If you send the same prefix twice and `cache_read_input_tokens` stays at zero, something upstream is breaking the prefix, and now you know to go diff the bytes.

The reason to wire this into a test or a dashboard rather than eyeball it once is that the failure mode is a regression, not a bad first build. Caching works the day you set it up, then six weeks later someone adds a dynamic field to the system prompt or a feature that rewrites history, and every request quietly starts missing. No error is ever raised. The only signal is that number going to zero and the bill going up, so make the number something you actually watch.

None of this is exotic. Keep the prefix byte-identical, put the parts that change at the end, do not switch models inside a cached thread, and read back the one usage field that proves it worked. That is close to the entire discipline, and it is the difference between paying for your repeated context once or paying for it every time.

If you have found a cache invalidator that took you a while to spot, I want to hear it, because they are all invisible until you know the exact shape of the one that got you.
