<!--
REVIEW NOTES (delete before publishing)
- COVER: cover.png
- Facts (research/2026-08-30-topic-scan.md): common Aug 2026 stack = frontier terminal agent (Claude Code or Codex) for heavy multi-file work + a free open-source agent (OpenCode, Cline) for lower-stakes tasks, connected through MCP. Real tools only.
- Ties to my routing/harness/MCP/coding-agent-router posts. NO META. aiscan PASS required.
- No AI-disclosure line (policy).
-->

---
title: "The 2026 coding setup isn't one agent, it's two: a frontier driver and a free open one"
published: false
description: "The stack that quietly became normal this year pairs an expensive terminal agent for heavy work with a free open-source one for everything else. It's routing, done at the human level."
tags: ai, agents, productivity, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-30-two-agent-coding-stack/cover.png
---

Somewhere over the past few months, my coding setup stopped being one AI agent and became two, and talking to other people I do not think I am unusual. The pattern that quietly became normal in 2026 is a pair: a frontier terminal agent like Claude Code or Codex for the heavy, multi-file, high-stakes work, and a free open-source agent like Cline or OpenCode for everything else, with MCP servers wiring them into the same tools. You reach for the expensive one when the task deserves it and the free one when it does not.

If that sounds familiar, it should. It is the same idea I keep circling from every angle, cheap by default and expensive on demand, except this time [the router is you](https://dev.to/frankchu/i-built-a-router-to-cut-my-claude-code-bill-and-prompt-caching-was-the-whole-problem-3ifl).

## Why two beats one

The single-agent instinct is to pick the best tool and use it for everything. That made sense when the gap between tools was large. It makes less sense now, because most of what you ask a coding agent to do is not hard. Rename this across the repo. Write the obvious test. Read this file and summarize what it does. Fix the import. Running a frontier agent for that work is like taking a taxi to your mailbox. It works, and you are paying for capability you are not using.

So people split the work. The frontier agent gets the tasks where judgment and blast radius are real: the cross-cutting refactor, the gnarly debugging, the design-sensitive feature. The free open agent gets the high-volume, low-stakes majority, where any competent model is fine and the cost of being wrong is small. You are not choosing which agent is better. You are matching the tool to the task, which is a different and smarter question.

The economics make it obvious once you feel it. The free agent handles the bulk of the calls at no marginal cost, so your spend concentrates on the small fraction of work that actually needs a frontier model. That is the same math behind every routing story I have written, just executed by hand instead of by a proxy. And the control is a bonus. The open agent runs on your terms, with your keys, on your machine, which is exactly where you want the routine, high-frequency work to live.

## MCP is the glue that makes it painless

The reason this is a real workflow and not just "have two apps open" is MCP. Because both agents can speak to the same MCP servers, they share tools. The same database connector, the same internal API, the same custom capability is available to whichever agent you hand the task to. You are not maintaining two separate integration setups. You build the tool layer once and both agents use it.

That is why the two-agent stack feels like one system instead of two. The [MCP roadmap I wrote about recently](https://dev.to/frankchu/the-mcp-roadmap-just-moved-from-tool-calling-to-running-agents-in-production-m86) is aimed squarely at this, at making the connective tissue around agents standard enough that mixing and matching agents is normal rather than painful. When your tools live behind MCP, swapping which agent does a task is a choice, not a migration, and that is what makes running two agents cheaper than the friction of running one.

## How I would actually set it up

If you want to try this, the shape is simple. Pick a frontier terminal agent as your driver for the hard stuff. Pick a free open-source agent as your workhorse for the routine stuff. Put your real tools behind MCP so both can reach them. Then build the habit that makes it work, which is pausing for half a second before a task to ask which agent this is. That habit is the whole skill. Most people default to the expensive agent for everything out of laziness, and that laziness is the entire cost.

The honest caveat is that two tools is more setup than one, and if you only code occasionally the single-agent simplicity might be worth more than the savings. This is a workflow for people who live in these tools daily, where the volume makes the routing pay off. But if that is you, the two-agent stack is the most practical version of the lesson I keep repeating: the model is a commodity, and the leverage is in how you route work across a tier of them. You can pay a proxy to do that routing, or you can build the instinct and do it yourself, one task at a time.

If you run a two-agent setup, I would like to hear where you draw the line between the driver and the workhorse, because that line is the actual decision and everyone seems to draw it a little differently.
