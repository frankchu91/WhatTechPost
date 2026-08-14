<!--
REVIEW NOTES (delete before publishing)
- Facts from TechCrunch/TheNextWeb/Cloudflare coverage (research/2026-08-12-topic-scan.md). Perf numbers are Cloudflare's own — phrased as their measurements.
- Optional upgrade: the beta is free via Browser Run on a Cloudflare account — a 30-min hands-on (one screenshot + one extraction through Playwright) would add a "tried it" section. Post works without it.
-->

---
title: "Cloudflare built a browser that throws away the screen"
published: false
description: "Kitesurf renders no pixels for humans: no tabs, no extensions, 7x less memory than Chromium. What a browser looks like when its only user is an agent."
tags: ai, webdev, cloudflare, agents
---

Every browser automation stack I've used — Puppeteer, Playwright, the agent tools built on them — shares one absurdity: it boots a full human browser, with its compositor and its 60fps scrolling and its extension machinery, so that a program can read some HTML. We've all just accepted that the tool for "fetch this page and find the price" is the same 300MB machine built for watching YouTube.

Cloudflare apparently stopped accepting it. Kitesurf, released this month in free beta, is a browser with no human affordances at all: no tabs, no themes, no extensions, no pixel-perfect rendering. It runs on Cloudflare Workers, written in Rust compiled to WebAssembly, and its stated design goals are the things an agent actually cares about — context windows, token costs, and cold-start speed.

## What's actually inside

The interesting part is that it isn't Chromium with features torn off. It's assembled from parts: the Blitz rendering engine, Firefox's Stylo CSS parser, and Boa, a Rust JavaScript engine. The architecture splits into an Engine that holds session state, a PageScript component that processes HTML/CSS/JS/WASM, and a PageRenderer that produces screenshots and PDFs only when asked.

Cloudflare's own numbers for the payoff: a screenshot costs 380ms of CPU against Chromium's 1,173ms, HTML extraction 229ms against 877ms, and memory lands around 39–58MiB where Chromium uses ~270MiB. Roughly 4x the speed at a seventh of the memory — their measurements, so apply the usual discount, but the direction is believable precisely because of everything they deleted.

The compatibility story is the pragmatic bit: it speaks the Chrome DevTools Protocol, so Playwright and Puppeteer scripts point at it without a rewrite. That's the difference between an interesting research artifact and something you can try this afternoon.

## Why this matters more than it looks

There's a pattern forming this month and Kitesurf fits it neatly. NVIDIA's NOOA treats an agent as a plain Python class. Switchyard treats model choice as a routing table. Kitesurf treats the browser as a headless extraction service. In each case, infrastructure that grew up around human interaction is being rebuilt around a different primary user, and the rebuilds are dramatically simpler than the originals — a browser gets 7x lighter when nobody's watching it.

The economics compound in an agent context. A browsing agent might touch fifty pages to answer one question; at Chromium weights that's a serious Workers bill and a serious latency tax. At Kitesurf weights it starts looking like ordinary API traffic. Cheap page access changes what agent designs are even worth attempting — polling-heavy patterns that were silly at 270MiB per page become reasonable at 40.

I'll note the strategic layer too, without cynicism: Cloudflare simultaneously sells bot protection to websites and now sells the infrastructure bots run on. They'd say verified agents and abusive scrapers are different populations, and the "agentic web" framing they're pushing — agents as first-class web citizens with their own identity — is genuinely the most coherent vision anyone's offered for how this ends up. But the same company arming both sides of an arms race is a detail worth keeping in view.

## Where I land

If you run browser automation inside an agent today, this is worth an afternoon: the CDP compatibility makes the trial nearly free, and the beta costs nothing. The thing I'd verify first — and what I'll test when I get to it — is JavaScript-heavy sites, because Boa is a young engine and the modern web leans hard on whatever V8 tolerates. A browser this light wins nothing if it can't parse the pages you actually need.

But the bigger takeaway stands regardless of whether Kitesurf specifically survives: we're watching the web grow a second interface, built for readers that never look at it. The browsers, the routers, the frameworks — the agent-native versions are all arriving at once, and they're all smaller than what they replace.

If you've pointed real Playwright workloads at it already, I'd like to hear the compatibility report.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
