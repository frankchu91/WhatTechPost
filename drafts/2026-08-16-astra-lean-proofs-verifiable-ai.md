<!--
REVIEW NOTES (delete before publishing)
- Facts from coverage of OpenAI's Aug 1 announcement (sources in research/2026-08-07-topic-scan.md). NOT independently verified: the zero-`sorry` claim (would require checking out the GitHub repo and running lake build — doable if you want, and would strengthen the post; consider adding actual verification).
- Math-community reaction is still developing — re-scan for expert commentary/refutations before publishing on ~Aug 16. If a proof gets challenged, that becomes the story.
- YOUR TAKE SLOT: [PERSONAL TAKE].
-->

---
title: "OpenAI's Astra solved 10 open math problems for $2,000 — but the real story is the zero-'sorry' Lean proofs"
published: false
description: "Forget 'AI does math.' The important part for developers: the output ships with machine-checkable proof certificates. That pattern is coming for your code."
tags: ai, programming, machinelearning, formalmethods
---

On August 1, OpenAI announced that Astra — its next model, still unreleased — produced solutions to ten math and theoretical CS problems that had been open for a decade or more. The headline result constructs a non-sofic group, answering a question posed by Gromov in 1999. Estimated compute cost for all ten: about **$2,000** in tokens.

Impressive. But "big model does hard math" is not the part that should interest you as a developer. The part that should interest you is *how the results shipped*: a 249-page manuscript **plus Lean 4 proof certificates on GitHub, Apache 2.0, with a `sorry` count of zero**.

## Why zero `sorry` is the whole story

If you haven't touched Lean: it's a proof assistant where `sorry` is the keyword for "trust me, I'll fill this in later" — the `TODO` of formal mathematics. A Lean development with zero `sorry` means every logical step of every proof is checked by the kernel, mechanically, no human trust required.

Which changes what "AI claims" even means. Nobody has to believe OpenAI. You can clone the repo and run the checker yourself. The claim isn't "our model is smart" — it's "here is an artifact whose correctness a machine verifies, produced by a machine." Whether Astra "understands" von Neumann algebras is now a philosophy question; whether the proofs are valid is a `lake build` away.

Notably, mathematicians *are* independently examining the published proofs right now — and that's the system working as designed. The verification story doesn't require trusting the announcement; that's the point.

## The pattern: generation is cheap, verification is the product

Here's the framing I keep coming back to: for years, the blocker on trusting LLM output has been that checking it costs as much as producing it yourself. Reviewing 500 lines of generated code is not obviously faster than writing them.

Formal certificates invert that. Generating the proof may have taken frontier-scale search; *checking* it takes minutes on a laptop, and the checker doesn't hallucinate. The expensive, fallible step and the cheap, reliable step have finally been separated.

That's not a math-only trick. It's the same shape as:

- Generated code shipping with **property-based tests the model must pass** (and that you spot-check)
- SQL migrations shipping with a **machine-checked equivalence proof** against the old schema
- Dependency updates shipping with **behavioral diff reports** instead of changelogs you take on faith
- An agent's PR shipping with a **typed contract** its changes provably satisfy

The common move: don't trust the model — make the model produce an artifact that a dumb, deterministic checker can validate. We already live by this pattern (types, tests, CI). The news is that models are now good enough to satisfy *much* stricter checkers than we currently deploy.

## The $2,000 number cuts both ways

$2,000 for ten decade-old open problems is absurdly cheap — postdoc-hours on any one of these cost more. But note what it implies about workflow: this was almost certainly massive parallel search with the Lean kernel as the filter, most of the spend going to attempts that got discarded.

That's the loop worth copying, at hobbyist scale: **generate many candidates, verify mechanically, keep survivors.** If your verification is trustworthy, model quality mostly changes your *bill*, not your correctness. I'd rather have a mediocre model and a great checker than the reverse.

Worth saying: none of the Clay Millennium Problems fell. There's a ceiling, and OpenAI's own framing acknowledges it. This is "search plus verification is further along than you thought," not "mathematicians are done."

[PERSONAL TAKE — where in your own stack could you swap "review the output" for "check a certificate"? One concrete place you'd apply generate-then-verify.]

## What I'd do with this

If you build with LLMs, steal the architecture: for any output that matters, ask *what's the cheapest deterministic checker that would catch a lie?* Sometimes it's a type system. Sometimes it's a test harness. Sometimes it's a whole proof assistant. The teams that get compounding value from models over the next few years will be the ones with the best checkers, not the best prompts.

Is anyone here already running formal verification against generated code in anger? I want to hear what broke.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
