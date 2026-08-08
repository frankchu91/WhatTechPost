<!--
REVIEW NOTES (delete before publishing)
- Leaderboard numbers as of early Aug 2026 (sources in research/2026-08-07-topic-scan.md). Re-check Terminal-Bench standings before publishing ~Aug 19; if a new model blew past 90, adjust the numbers, the thesis survives.
- This is the opinion piece — it lives or dies on YOUR voice. The [PERSONAL TAKE] slots here are not optional; fill both.
- Good discussion-bait: expect pushback from "model quality is everything" folks. That's the point.
-->

---
title: "Coding agents have converged. Your harness now matters more than your model"
published: false
description: "89.5 vs 89.1 on Terminal-Bench 2.1. When the top models are half a point apart and prices are collapsing, the differentiation moved into the loop around the model."
tags: ai, programming, productivity, devtools
---

Here's the number that reframed my month: on Terminal-Bench 2.1, GPT-5.6 Sol scores **89.5%** and Claude Opus 5 at max effort scores **89.1%**. The default models of the two most-used coding agents are within *half a point* of each other.

Meanwhile, Opus 5 launched at half its flagship predecessor's price, OpenAI cut mid-tier prices by up to 80%, and open-weights models got cheap enough to run coding agents for cents.

Model race: effectively tied. Price race: collapsing. So where did the actual competition go? Into everything *around* the model — and if you're still picking tools by benchmark scores, you're optimizing the solved part of the problem.

## What "harness" actually means

The harness is everything between the model and the outcome: what context gets loaded and when, how the agent verifies its own work, what it's allowed to do without asking, how it recovers from being wrong, and what it remembers across sessions.

The last few months of coding-agent news is all harness news, not model news: Claude Code shipped a security scanner into the terminal; the ecosystem argument moved to skills, hooks, and sandboxing; the recurring Hacker News complaint isn't "the model is dumb," it's "the agent lost my context / edited the wrong thing / didn't run the tests." None of those are fixed by 0.4 more benchmark points.

## Why half a point doesn't survive contact with your repo

Benchmarks measure the model alone on self-contained tasks. Your Tuesday is different: a legacy repo with implicit conventions, tests that take four minutes, a deploy step that isn't in any README. On that terrain, harness quality dominates:

- A worse model that **runs your tests after every change** beats a better model that doesn't.
- A worse model with **your project's conventions in context** beats a better model guessing from vibes.
- A worse model that **can safely try three approaches in an isolated worktree** beats a better model that gets one shot in your working directory.

Every one of those is a harness property. You control them; the vendors' half-point isn't in your control at all.

[PERSONAL TAKE #1 — a concrete moment where harness beat model for you: the same task failing on default settings and succeeding after you fixed context/verification/permissions.]

## The uncomfortable part: your setup is the moat now

The convergence has a personal-productivity implication people are dancing around: two developers using the *same* agent on the *same* model are no longer getting remotely the same results. The gap between "types a prompt and hopes" and "maintains a CLAUDE.md, wires up test hooks, curates skills" is now larger than the gap between any two frontier models.

That's genuinely new. In 2024, tool choice was most of the variance. In 2026, *configuration* is most of the variance. Which means the "which agent is best" debate is mostly a proxy war — the honest question is "whose harness discipline is best," and that one has an uncomfortable answer for most of us.

My working list, in order of return on effort:

1. **Verification loops** — the agent runs tests/linters itself, always. Biggest single win.
2. **Written-down conventions** — a good agent-instructions file beats a model upgrade.
3. **Safe parallelism** — isolated worktrees so the agent can be wrong cheaply.
4. **Context curation** — what the agent *doesn't* see matters as much as what it does.

[PERSONAL TAKE #2 — your ranking, and the one investment that most changed your daily output.]

## Where this goes

Models will keep leapfrogging each other by half-points, and switching costs between them are heading toward zero — that's what price wars and converged scores mean. Harnesses are the opposite: they accumulate. Every hook, convention file, and verification loop you build compounds across every future model you plug into it.

Invest accordingly.

Tell me I'm wrong in the comments — specifically, tell me about a task where a model swap alone, same harness, made the difference. Those counterexamples are the most useful data I could get.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
