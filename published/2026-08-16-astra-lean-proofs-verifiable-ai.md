<!--
REVIEW NOTES (delete before publishing)
- Rewritten 2026-08-12 in the new voice (see VOICE.md).
- Facts from coverage of OpenAI's Aug 1 announcement (sources in research/2026-08-07-topic-scan.md). Not independently verified: the zero-`sorry` claim. Cloning the repo and running the checker before publishing would strengthen the post — the text currently says honestly that we haven't.
- Re-scan for math-community reactions before publishing; if a proof gets challenged, that becomes the story.
-->

---
title: "The interesting part of the Astra math news isn't the math"
published: false
description: "OpenAI's model solved ten open problems, but what stuck with me is how the results shipped: proof files a machine can check. That pattern applies to code too."
tags: ai, programming, machinelearning, formalmethods
---

When OpenAI announced earlier this month that its unreleased Astra model had solved ten open math problems, I almost scrolled past. "Big model does impressive thing" is background noise at this point, and I have no way to evaluate a result about non-sofic groups anyway. I'd guess most working developers are in the same position.

What made me stop was a detail further down: the results didn't ship as a paper and a press release. They shipped as a 249-page manuscript plus Lean 4 proof certificates, on GitHub, under Apache 2.0. And the repository's `sorry` count is zero.

That detail has been rattling around in my head for two weeks now, because I think it describes a workflow the rest of us are going to end up using — not for math, for ordinary code.

## What zero `sorry` means

If you haven't used Lean: it's a proof assistant, and `sorry` is its keyword for "trust me, I'll prove this part later." It's the `TODO` of formal mathematics. A Lean development with no `sorry` anywhere means every logical step of every proof has been checked mechanically by the kernel. No referee's patience involved, no benefit of the doubt.

Which changes what the announcement even is. Nobody has to believe OpenAI's claims about their model. You can clone the repository and run the checker on your own laptop, and mathematicians are doing exactly that right now. Whether Astra "understands" von Neumann algebras is a philosophy question. Whether the proofs are valid is a build command.

I haven't run the checker myself yet — it's on my list, and I'll add an update here when I do. But the shape of the thing is what interests me, and the shape doesn't depend on my laptop.

## Generation is cheap now; verification is the product

The blocker on trusting LLM output has always been that checking it costs about as much as doing the work yourself. Reviewing five hundred generated lines is not obviously faster than writing them. This is why "the model wrote it" still makes people nervous, and why it should.

The Astra release inverts that arithmetic. OpenAI estimated the compute for finding all ten solutions at around $2,000 — which means the workflow was almost certainly a huge parallel search where the Lean kernel filtered out every wrong attempt, and most of the money went to discarded candidates. Generating a proof took frontier-scale search. Checking it takes minutes, and the checker doesn't hallucinate.

The expensive, fallible step and the cheap, reliable step got separated. That's the whole trick, and it's not a math-specific trick. We already live by a weaker version of it: types, tests, CI. The news is that models are now good enough to satisfy much stricter checkers than the ones we currently point them at.

<!-- PERSONAL TAKE: a concrete place in your own stack where you could swap "review the output" for "check a certificate" — even a small one. -->

## What I'm taking from it

Since reading about it I've been asking one question about every LLM-generated artifact in my own projects: what's the cheapest deterministic check that would catch a lie here? Sometimes the answer is a type signature. Sometimes it's a property-based test the generated code has to pass. It's rarely "a human reads it carefully," which is the check I was implicitly relying on before.

For what it's worth, none of the Clay Millennium Problems fell, and OpenAI's own framing acknowledges the ceiling. This isn't "mathematicians are done." It's narrower and more useful than that: generate many candidates, verify mechanically, keep the survivors — and the quality of your checker matters more than the quality of your generator.

If you're already running generated code against anything stricter than unit tests, I'd genuinely like to hear how it's going.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
