<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-25-mcp-roadmap.png
- Facts (research/2026-08-25-topic-scan.md): MCP 2026 roadmap five priorities — agentic messaging (server events, Tasks extension), stateless HTTP transport (Google-proposed, for Cloud Run/K8s), agent identity & security (DPoP, Workload Identity Federation, token exchange, sub-agent delegation), progressive tool discovery, SDK DX.
- Written to pass aiscan (few em-dashes, minimal bold). Re-run node scripts/aiscan.js before publishing.
- No AI-disclosure line (policy).
-->

---
title: "The MCP roadmap just moved from tool-calling to running agents in production"
published: false
description: "The new Model Context Protocol roadmap is about identity, delegation, stateless transport, and progressive discovery. It reads like a to-do list for agents that outgrew the demo."
tags: ai, agents, webdev, opensource
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-25-mcp-roadmap.png
---

The Model Context Protocol spent its first year being the thing that let a model call your tools. The new roadmap is about something harder, and if you build agents it is the more useful document: how those tools survive contact with production, scale, and more than one agent talking at once. The five priorities read less like a protocol wishlist and more like a list of everything that breaks once an agent stops being a demo.

Here is what changed, and why each item is really a scar from running agents for real.

## Identity and delegation: agents need to log in as themselves

The headline shift is agent identity. Today an MCP server mostly assumes a human is behind the request. The roadmap adds a way for a server to be reached by an agent acting as itself, or as a user who delegated access to it, with real machinery behind it: DPoP, Workload Identity Federation, token exchange.

That sounds like plumbing until you picture the actual situation it fixes. An autonomous agent runs overnight, spins up sub-agents, and each one needs to authenticate to your systems and prove what it is allowed to touch, with no human awake to click "approve." Right now people solve that by handing agents a human's credentials, which is exactly the Excessive Agency problem the OWASP list just promoted. Giving agents their own scoped identity is the difference between an audit trail and a shrug when something goes wrong.

## Stateless transport: the boring fix that matters most

The least glamorous item is the one I would watch first. Today's streamable HTTP transport is stateful, which pins a session to a specific server process and makes it painful to run on the horizontally scaled infrastructure everyone actually deploys on. Google proposed a stateless transport that removes the pinning, so MCP servers run cleanly on Cloud Run, Kubernetes, and anything else that scales by adding identical boxes.

I keep coming back to this because it is the item that decides whether MCP is a laptop protocol or a production one. A stateful transport is fine when you run one server for yourself. It falls apart the moment you need ten of them behind a load balancer. Fixing that is not exciting, and it is the precondition for everything else on the list.

## Progressive discovery: stop drowning the model in tools

Progressive tool discovery lets a server reveal its tools gradually instead of dumping hundreds into the model's context at startup. Anyone who has connected a real agent to a rich MCP server has felt this. The tool list alone eats the context budget, and the model gets worse at choosing because it is staring at a wall of options it will never use for this task.

Revealing tools as they become relevant is the same instinct behind good API design and good menus. Show the ten things that matter now, not the two hundred that might matter someday. It also quietly improves accuracy, because a smaller, task-relevant tool set is one the model can actually reason about.

## What it tells you about where agents are

Line the five priorities up. Async task primitives for long-running work. Stateless transport for scale. Identity and delegation for autonomy. Progressive discovery for context discipline. Better SDKs so people can build all of it. Not one of them is about making a model smarter. Every one is about making the connective tissue around agents trustworthy enough to run without a person watching.

That is the same story I keep writing from different angles. The model is the commodity, and the hard, valuable work has moved into the layer around it. MCP's roadmap is that thesis expressed as a standards body's backlog, which is about as official as a signal gets. If you are building agents, this is the map of what production actually demands, written by the people watching it break. Read it as a checklist for your own stack, because these are the problems you are going to hit whether or not the protocol solves them for you first.

If you have already worked around one of these, especially agent identity, I would like to hear what you did before the standard caught up. Those workarounds are where the real lessons live.
