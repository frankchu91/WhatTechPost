<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-25-harness-rankings.png
- Facts (research/2026-08-24-topic-scan.md): CellCog / LogRocket Aug 2026 rankings — Claude Code #1 for hooks/subagents/dynamic workflows, default for long autonomous coding; Codex CLI for cloud/PR-shaped autonomy; Cursor leads in-editor; Claude Code on Opus 5 (near-flagship at ~half price, per-request effort dial, per-subagent model control).
- Ties to my convergence post (harness > model). Cross-link it: https://dev.to/frankchu/i-went-looking-for-a-reason-to-switch-coding-agents-and-couldnt-find-one-27m1
- Keep tool-agnostic and fair; not an ad for Claude Code.
- No AI-disclosure line (policy).
-->

---
title: "People are ranking agent harnesses now, not just models. That's the whole shift in one headline"
published: false
description: "New coding-agent rankings score tools on hooks, subagents, and workflow control — not model quality. When the leaderboard is about the harness, the harness is the product."
tags: ai, agents, productivity, devtools
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-25-harness-rankings.png
---

A small thing in this month's dev-tool coverage says more than the big model launches did: the rankings that matter for coding agents have quietly stopped being about models and started being about harnesses. CellCog's August ratings put Claude Code first for depth of hooks, subagents, and dynamic workflows. Codex CLI gets called out for cloud, pull-request-shaped autonomy. Cursor leads for in-editor flow. Notice what's being scored — not "whose model is smartest," but whose *scaffolding* around the model is best.

I wrote a couple of weeks ago that I went looking for a reason to switch coding agents and couldn't find one, because the models had converged and my own configuration explained more of my results than the model did. These rankings are that argument showing up as an industry norm.

{% link https://dev.to/frankchu/i-went-looking-for-a-reason-to-switch-coding-agents-and-couldnt-find-one-27m1 %}

## What "ranking the harness" actually measures

Look at the axes and they're all harness properties, not model properties. Hooks: can the tool run your tests, your linters, your checks automatically at the right moments? Subagents: can it spin up scoped helpers with their own instructions and — in Claude Code's case now — their own model per subagent? Dynamic workflows: can it plan, branch, and recover across a long task instead of one-shotting? Effort control: can you dial reasoning up for the hard step and down for the cheap one?

None of that is "the model." All of it is the machine you build around the model, and it's exactly the stuff that determines whether an agent survives contact with a real repo. A ranking that scores these things is admitting, in public, that the model is now the commodity and the harness is the differentiator. The same base model behaves like a different product depending on the scaffolding it's dropped into — which is why one tool can top the chart and another can frustrate you, on identical underlying weights.

## The Opus 5 detail that proves the point

The single most telling feature in the writeup isn't a benchmark — it's *per-subagent model control*: the ability to assign different models to different subagents inside one task. Cheap fast model for the mechanical steps, expensive careful model for the step that needs judgment, all inside a single run.

That's routing, built into the harness, and it's the same idea I keep bumping into from every direction — the escalation router I tested locally, the Switchyard proxy, "small model by default, big model on demand." When your coding agent lets you assign models per subagent, the tool has absorbed the routing layer into itself. The harness isn't just around the model anymore; it's orchestrating *several* models, and choosing between them is now a configuration you own. That's a different job than "pick the best model," and it's the job that actually moves your results.

## What I'd do with this

Stop shopping for the best model and start investing in your harness, because that's what the rankings are quietly telling you to do. Concretely, in whatever agent you use: get your test/lint hooks wired so verification is automatic, learn the subagent and effort controls instead of leaving them on defaults, and write down your project conventions where the agent can read them. Those four things will move your day more than any model swap on offer this quarter.

And read harness rankings the way they're meant: not as "which tool is best" but as "which capabilities matter" — hooks, subagents, routing, recovery. Then make sure you're actually using the ones your tool already has. Most people are leaving the ranked features switched off.

Which harness capability changed your results the most once you actually turned it on? I'm collecting these, because the gap between a tool's defaults and its configured potential is the least-discussed number in this whole space.
