<!--
REVIEW NOTES (delete before publishing)
- COVER IMAGE: assets/2026-08-22-eu-ai-act.png
- Facts (research/2026-08-19-topic-scan.md): Article 50 transparency duties in effect Aug 2 2026; disclose AI interaction + machine-readable marking of AI-generated content; penalties up to 3% of global turnover. VERIFY specifics before publishing — EU AI Act details are easy to get subtly wrong; keep claims at the level the sources support and link the official text. Don't give legal advice; frame as "what I'm doing / what devs should check."
- Practical checklist angle for developers shipping AI features.
-->

---
title: "The EU AI Act's disclosure rules are live now, and they apply to your side project too"
published: false
description: "Article 50 took effect August 2: label AI interactions, mark AI-generated content machine-readably. Penalties reach 3% of global turnover. A builder's plain-English checklist."
tags: ai, webdev, legal, career
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-22-eu-ai-act.png
---

A rule that's easy to ignore until it isn't: the EU AI Act's [Article 50](https://artificialintelligenceact.eu/transparency-rules-article-50/) transparency obligations took effect on August 2. If your app talks to EU users — and if it's on the open internet, it probably does — a few of its requirements now apply to you, indie side project or not. Fines for breaking this tier of the Act run up to €15 million or 3% of worldwide annual turnover, whichever is higher — a scary number, though realistically not aimed at your weekend app. Still, the obligations are real and the fixes are small, so there's no reason to be on the wrong side of them.

I'm a developer, not a lawyer, and this isn't legal advice — treat it as a prompt to go read the actual text or ask someone who does this for a living. But here's the plain-English version of what changed and what I'm doing about it.

## The two obligations that touch most builders

Article 50 is broad, but two pieces catch almost everyone shipping AI features.

First: if a user is interacting with an AI system, you have to tell them — unless it's obvious. A chatbot that's clearly a chatbot may be fine; a support widget that quietly hands off to an AI, or a "person" in your app that's actually a model, is exactly what this targets. The bar is that a reasonable user should know they're talking to a machine.

Second: AI-generated content has to be marked as such in a machine-readable way. Not just a visible "made with AI" label for humans — a marking that other software can detect, so the content stays identifiable as it moves around the internet. This is the one developers underestimate, because it's a technical requirement, not a copy change. Think metadata, watermarks, provenance signals — the machine-readable part is doing real work in the text.

One bit of breathing room on this second one: there's a transitional period. For generative systems already on the market, the marking-and-detection obligation doesn't bite until December 2, 2026 — so you have a runway to get provenance marking in place. The interaction-disclosure obligation, though, applies now, from August 2, with no grace period. Don't let the December date lull you on the part that's already live.

## The plain-English checklist

Here's what I'd actually walk through for a project that uses AI:

Does a user ever interact with a model without clearly knowing it? If yes, add disclosure — a line of copy, a badge, whatever makes it unambiguous. Cheap to fix, easy to forget in the flows where the AI is *behind* something.

Do you generate content users might take for human-made or authentic — images, text, audio, video? If yes, you're in machine-readable-marking territory. Look at what your generation provider already emits (many now attach provenance metadata like C2PA by default) and don't strip it in your pipeline. Half of compliance here might be "stop removing the marking that's already there."

Are you deep-faking or synthesizing anything resembling a real person or real events? That's the sharp end of the rules and where you should stop reading blog posts and talk to counsel.

## Why I think this is worth ten minutes, not zero

It's tempting to treat regulation as big-company homework. But two things make Article 50 different for small builders. The disclosure obligations don't have a startup carve-out the way some rules do — they attach to the practice, not the company size. And the fixes are genuinely small: a disclosure line and not stripping provenance metadata cover most everyday cases.

There's also a straightforwardly good version of this. "Tell people when they're talking to AI" and "keep AI-generated media identifiable as it spreads" are things I'd want as a user regardless of the law. The regulation is forcing a baseline of honesty that the ecosystem arguably should have adopted on its own. I'd rather build on the compliant side by default than retrofit it after the rules grow teeth in the markets I care about.

Go read the real text before you rely on any of this — but don't file it under "later." The obligations are live today.

If you've already added AI-disclosure to a product, what did you actually change? I'd like a running list of what compliance looks like in practice versus on paper.
