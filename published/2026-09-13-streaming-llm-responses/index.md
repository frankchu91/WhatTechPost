<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/13 post 1/3. FORMAT: practical/hands-on AI-building (streaming UX + gotchas).
- Facts general/verifiable: SDKs expose a stream helper (.get_final_message/.finalMessage); streaming avoids HTTP timeouts on long/large outputs; don't parse partial JSON mid-stream; handle cancellation. Keep provider-neutral-ish, Claude examples fine.
- aiscan-clean; no banned words in comment. NON-META (no Meta needed). No AI-disclosure line. COVER: cover.png.
-->

---
title: "Streaming an LLM response is easy. The parts that bite come after the first token."
published: false
description: "Streaming makes an app feel fast and dodges timeouts on long outputs. It also breaks partial parsing, complicates cancellation, and hides errors mid-stream. Here's the whole picture."
tags: ai, llm, programming, webdev
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-13-streaming-llm-responses/cover.png
---

Streaming is the difference between an app that feels instant and one where the user stares at a spinner for eight seconds. The model sends tokens as it generates them, you show them as they arrive, and the perceived speed changes completely even though the total time is the same. Turning it on is a one-line change in most SDKs. The things that bite you all show up after the first token, so here is the full picture before you ship it.

## Why stream at all

Two reasons, and the second is the one people forget. The obvious one is feel: partial output on screen reads as fast, a blank wait reads as broken, even at identical latency. The less obvious one is that streaming is how you avoid HTTP timeouts on long responses. A large generation can run past a client's request timeout and die on a non-streaming call, while the same request streamed keeps the connection alive token by token. If you ask for a big output, stream it, or budget for the timeout.

Use the SDK's stream helper rather than hand-rolling event handling. Most clients give you something like a `get_final_message` that accumulates the stream and hands back the complete response, so you get the live tokens and the assembled result without wiring up raw events yourself.

## Do not parse partial output mid-stream

The sharpest trap. If the model is streaming JSON and you try to parse the buffer on every chunk, you will feed `json.loads` a half-written object and it will throw, or worse, occasionally succeed on a truncated shape and hand you wrong data. Streamed text is valid only when the stream completes. Show partial text to the user if you like, but do not act on structured output until the final token has landed. If you need both structure and streaming, stream for the user-visible text and parse once at the end, or use a constrained-output mode and still parse only when done.

## Errors can arrive after you have shown output

A non-streamed call fails cleanly: you get an exception, you handle it. A streamed call can start fine, emit two hundred tokens, and then error. Now you have half an answer on the user's screen and a failure to handle. Decide the behavior up front. Usually that means catching the mid-stream error, marking the message as incomplete in the UI, and offering a retry, rather than leaving a truncated response sitting there looking finished. The failure is not rarer with streaming, it just arrives later and messier.

## Cancellation is a feature, not an afterthought

Streaming makes it possible to stop generation partway, which users expect the moment they see text appear, and which saves you output tokens on abandoned requests. Wire the cancel path through: when the user navigates away or hits stop, actually abort the stream and close the connection instead of letting it run to completion in the background billing you for tokens nobody will read. On a busy app this is a real line on the invoice, not a nicety.

## The retry wrinkle

A dropped stream does not retry cleanly, which is worth saying twice because it interacts with everything above. If you have already shown output and the connection drops, a naive retry restarts from the first token and the user sees the answer stutter or double. Either buffer until complete before showing anything, which gives back some of the perceived-speed win, or design the UI to replace rather than append on a restart. Pick one deliberately.

Streaming is worth it. The feel is better and the timeout problem goes away. Just remember that everything after the first token, parsing, errors, cancellation, retries, is a little harder than the non-streamed version, and that difficulty is the actual work. The one-line change turns it on. The handling is what makes it production.

If you have a streaming bug that only showed up with real users, I want to hear it, because the mid-stream failures are the ones no demo ever surfaces.
