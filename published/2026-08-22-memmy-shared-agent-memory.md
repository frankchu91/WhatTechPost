<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-22-memmy.png
- Facts (research 2026-08-19/20): MemTensor/memmy-agent, open-source, local-first shared memory hub; supports Claude Code, Codex, Cursor, OpenClaw, Hermes; auto-scans existing agent history; memory layers L1 Trace / L2 Policy / L3 World Model / Skill; desktop app + CLI + OpenAI-compatible API.
- HANDS-ON OPPORTUNITY: this is installable — a real "I pointed it at my agent history and here's what it built" section would make this the strongest post of the week. Left as analysis with an honest "going to run it" frame; upgrade before publishing if you have 30 min.
- No AI-disclosure line (policy).
-->

---
title: "Your AI agents each have amnesia. Memmy tries to give them one shared memory"
published: false
description: "An open-source, local-first memory hub that lets Claude Code, Codex, and Cursor draw on the same context about you — instead of every tool starting from zero."
tags: ai, agents, opensource, productivity
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-22-memmy.png
---

Here's a papercut I've stopped noticing because it's constant: every AI tool I use starts from zero. Claude Code doesn't know what I told Codex yesterday. Cursor has never met either of them. I re-explain the same project conventions, the same preferences, the same "we don't do it that way here" three times to three tools that will all forget by next week. Each one is individually smart and collectively amnesiac.

Memmy, an open-source project from MemTensor, is a swing at exactly that problem, and the framing is the interesting part: not memory *for an agent*, but one memory *shared across all of them*.

## What it actually is

Memmy is a local-first memory hub. It runs on your machine, and it exposes your accumulated context to whatever agents you point at it — the README lists Claude Code, Codex, Cursor, OpenClaw, and Hermes. The pitch that got my attention: after you install it, it can scan the history of your *existing* agents and convert months of accumulated project context, work habits, and preferences into a shared long-term memory, in minutes. You're not starting the memory from scratch; you're harvesting what's already scattered across your tools.

The architecture is more thought-through than "throw it all in a vector DB," which is where most memory tools stop. Memmy separates memory into layers: L1 Trace is the raw material — requests, responses, tool calls. L2 Policy is the distilled version — recurring patterns, rules, things that went wrong and shouldn't again. L3 World Model is stable knowledge about your context and constraints. And a Skill layer captures SOP-like workflows learned from experience. That's a real hierarchy: raw history at the bottom, hard-won rules and workflows at the top, with the useful stuff promoted upward instead of drowning in logs.

It ships as a desktop app, a CLI, and — the detail that makes it composable — an OpenAI-compatible API, so anything that speaks that protocol can read from the same memory.

## Why the layering is the whole point

I've tried the "just give the agent a memory file" approach, and the failure mode is always the same: the file grows, and growth is the enemy. A flat memory becomes a haystack, and the agent spends its context budget re-reading things that don't matter to the task in front of it. Raw history is nearly worthless past a certain size precisely because it's undifferentiated.

Memmy's layers are a bet that the fix is *distillation*, not accumulation. The L2 Policy layer — "here are the rules you've learned, separate from the thousand conversations you learned them in" — is the one I'd want most, because it's the difference between an agent that remembers *what happened* and one that remembers *what to do*. Whether Memmy's distillation is actually good is the thing I'd test first; a memory hierarchy is only as useful as the promotion logic that decides what rises to the top.

## The honest caveats

Local-first is the right call for something that ingests your entire work history — that data should not leave your machine, and it's genuinely good that Memmy's default keeps it home. But pointing any tool at "the complete history of everything I've asked my agents" is a real trust decision, open-source or not. Read what it stores and where before you feed it your life.

And shared memory across tools cuts both ways: a wrong or stale "rule" in the Policy layer now poisons every agent at once instead of just one. Centralizing memory centralizes its mistakes. That's a fair trade for not re-explaining yourself constantly — but it means the memory needs curation, not just accumulation, and that's work you can't fully outsource to the tool.

I'm going to point it at my own agent history and see what it builds — the L2 Policy layer especially, because if it distills my scattered corrections into something reusable, that's the papercut finally closing. If you've run it, I'd like to hear whether the shared memory actually made your tools feel like they know you, or just gave them more to read.
