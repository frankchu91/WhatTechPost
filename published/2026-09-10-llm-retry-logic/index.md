<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 1 of 3 (9/10), post 1/3. FORMAT: practical/hands-on AI-building.
- Facts verified vs Claude API error-handling docs: official SDKs auto-retry 408/409/429/5xx + connection errors (default ~2 retries) with backoff; honor Retry-After; non-retryable = 400/401/403/404. Anthropic overload = 529. Timeouts retried -> wall-clock stacks. Keep claims general/accurate; don't overstate exact per-provider numbers.
- Keep aiscan-clean (no swap-table tell-words here either). NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "Your LLM calls need real retry logic, and the SDK only does half of it"
published: false
description: "A 429 under load, a 529 overload, a dropped stream. The official client retries some of that for you. The parts it can't, idempotency, wall-clock caps, and what not to retry, are on you."
tags: ai, llm, python, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-10-llm-retry-logic/cover.png
---

An LLM API call fails at the worst possible moment. A 429 when your traffic spikes, a 529 when the provider is overloaded, a connection that drops halfway through a stream. A naive app turns that into a user-facing error, or worse, a half-finished action it never retries. Retry logic is the difference, and most of what people write by hand is either redundant with the SDK or subtly wrong.

Here is what actually needs handling.

## Know what the SDK already does

The official clients are not bare HTTP. By default they retry the transient failures for you, 429, the 5xx family, connection errors, usually a couple of times, with exponential backoff, and they honor the `Retry-After` header when the server sends one. So the first move is not to write a retry loop. It is to read your client's defaults and raise the retry count or timeout if your workload needs it, rather than reimplementing backoff badly on top of backoff that already works.

What the SDK cannot decide for you is everything that depends on your application, and that is the part worth writing.

## Retry the right failures, and only those

Split errors into two piles. Retryable: 429 rate limits, 529 overloads, 500-class server errors, timeouts, and connection drops. These are transient and a later attempt can succeed. Not retryable: 400 bad request, 401 and 403 auth problems, 404. Retrying those just burns time and money while the result stays identical, because the problem is your request, not the server's mood. Catch a specific chain, not one broad exception, so a 404 fails fast while a 429 backs off.

## Cap the wall clock, not just the attempts

A subtle trap: timeouts are themselves retried, so "3 retries" with a 60-second timeout can mean three minutes of a user waiting on one call. Bound the total time, not only the attempt count. Add jitter to the backoff so a fleet of workers that all failed at once does not retry in lockstep and hammer the provider at the same instant.

```python
import random, time

RETRYABLE = {429, 529, 500, 502, 503, 504}

def call_with_retry(make_request, attempts=4, cap_seconds=45):
    start = time.monotonic()
    for i in range(attempts):
        try:
            return make_request()
        except HttpError as e:
            if e.status not in RETRYABLE or i == attempts - 1:
                raise
            if time.monotonic() - start > cap_seconds:
                raise
            wait = min(2 ** i, 8) + random.uniform(0, 0.5)  # backoff + jitter
            time.sleep(e.retry_after or wait)               # honor Retry-After
```

## The two failures people forget

Streaming does not retry cleanly. If you have already shown the user 200 tokens and the stream drops, a naive retry restarts from zero and the user sees a stutter or a doubled answer. Decide up front: buffer until the stream completes, or design the UI to tolerate a restart.

Retries can double-fire side effects. If the call triggers an action, sends an email, charges a card, books a slot, a retry after a timeout can run it twice, because the first attempt may have succeeded before the connection died. Make the operation idempotent, or dedupe on a key you control, before you add a single retry.

Retry logic is easy to feel done with after one `try/except` and a `sleep`. The version that survives production knows which errors to retry, stops burning time on the ones it cannot fix, bounds the total wait, and never fires a side effect twice. The SDK gives you the backoff. The judgment is the part you own.

If you have a retry bug that only showed up under real load, I want to hear it, because that is where the gap between a demo and a product always turns out to be.
