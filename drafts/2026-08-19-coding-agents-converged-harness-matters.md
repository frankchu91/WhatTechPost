<!--
REVIEW NOTES (delete before publishing)
- COVER IMAGE (dev.to editor "Add a cover image"): assets/2026-08-19-convergence.png
- Rewritten 2026-08-12 in the new voice (see VOICE.md).
- Leaderboard numbers as of early Aug 2026 (sources in research/2026-08-07-topic-scan.md). Re-check Terminal-Bench standings before publishing; if a new model blew past 90, adjust the numbers — the argument survives.
- The two PERSONAL TAKE comments are where your real setup stories go; the post works without them but is much better with them.
-->

---
title: "I went looking for a reason to switch coding agents and couldn't find one"
published: false
description: "The top models are half a benchmark point apart now. What I found instead was that my own configuration explains more of my results than the model does."
tags: ai, programming, productivity, devtools
---

A few evenings ago I sat down to figure out whether I should switch coding agents. New benchmark numbers were out, prices had just moved again, and I had that vague feeling that everyone else was using something better than me.

The research didn't go the way I expected. On Terminal-Bench 2.1, GPT-5.6 Sol scores 89.5% and Claude Opus 5 at max effort scores 89.1%. Those are the default models behind the two most-used coding agents, and they are four tenths of a point apart. Meanwhile Opus 5 launched at half its predecessor's price, and OpenAI cut its mid-tiers by up to 80% a couple of weeks ago. The models have converged and the prices are collapsing, at the same time.

So I closed the comparison tabs, and I've been thinking since about where my results actually come from. The uncomfortable answer is that most of the variance lately hasn't come from the model at all. It's come from everything I've wired up around it.

## What actually moved the needle for me

I keep an instructions file in each project — conventions, what to run, what not to touch. The weeks where those files are good, the agent is good. The weeks where they've drifted out of date, the agent confidently does last month's right thing.

Same with verification. The single biggest improvement I ever made to my agent setup wasn't a model upgrade; it was making test runs non-optional, so the agent checks its own work before I see it. A weaker model that runs the tests beats a stronger model that doesn't, and it isn't close. Benchmarks can't see this, because benchmarks come with their own harness — they measure the model alone on self-contained tasks. Your repo, with its four-minute test suite and its deploy step that isn't written down anywhere, is a different kind of terrain.

<!-- PERSONAL TAKE: a specific moment when fixing your setup (context file, test hook, permissions) changed the outcome on a task the model had been failing. -->

## The part I find uncomfortable

Here's the thing I'd been avoiding admitting: two developers using the same agent on the same model are no longer getting remotely similar results. The gap between someone who types a prompt and hopes, and someone who maintains their conventions file, wires up test hooks, and curates what the agent can see — that gap is now wider than the gap between any two frontier models.

In 2024, tool choice explained most of the difference. In 2026 it's configuration discipline, which is a less fun thing to be told, because you can't fix it by switching products. I say this as someone whose own conventions files were embarrassingly stale when I finally looked.

If I rank what's been worth the effort, for me it's been: verification loops first, written-down conventions second, letting the agent work in an isolated worktree so it can be wrong cheaply third, and trimming what goes into context last. Your order may differ, but I'd be surprised if "which model" cracked the top three.

<!-- PERSONAL TAKE: your own ranking, or the one investment that most changed your daily output. -->

## Where this leaves me

I didn't switch. Not out of loyalty — the models are close enough that switching costs would exceed any difference, and that's exactly what converged scores and price wars mean. The models will keep leapfrogging each other by half-points. The stuff around them accumulates: every hook, convention file, and verification loop keeps paying off across whatever model I plug in next year.

If you've seen the opposite — a task where swapping the model alone, same setup, made the real difference — I'd honestly like to hear about it. That's the counterexample my thinking needs.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
