<!--
REVIEW NOTES (delete before publishing)
- FORMAT: discussion (提问式), discuss tag. Short (~600 words). Reader-first, ends on real questions. Our first real discussion post (highest-comment format on dev.to per the top-post data).
- Relatable topic every AI-coding dev faces daily; invites people to share their own setup in comments.
- Keep aiscan-clean; do NOT list banned words in this comment (scanner reads it). No personal-take slot. NON-META. No AI-disclosure line. COVER: cover.png (OPINION).
-->

---
title: "Every new session, your AI agent starts from zero. What do you actually feed it to catch up?"
published: false
description: "A fresh session and the agent knows none of your conventions, none of yesterday's decisions. We all built a patch for this. I want to compare what's actually in yours."
tags: discuss, ai, productivity, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-07-agent-context-between-sessions/cover.png
---

You open a fresh session and your coding agent knows nothing. Not your naming conventions, not the decision you made yesterday, not why that one function carries a comment that says "do not touch, see incident." It is a sharp new hire with total amnesia, every single morning.

So all of us built some patch for this, and I do not think anyone is sure theirs is good. Here is the spread I keep seeing, where I have landed, and then I want yours.

## The usual approaches

The project file. A `CLAUDE.md`, a `.cursorrules`, an `AGENTS.md` at the repo root that the tool reads on every session. Cheap, versioned, shared with the team. The failure mode is that it rots the moment nobody updates it, and a confident wrong instruction is worse than no instruction.

The pasted preamble. You keep a block of context in a note and paste it at the start of a session. Flexible, but manual, and you are back to copy-paste as a lifestyle.

The memory server. An MCP memory layer or a vector store the agent queries for past context. Powerful, and also the most ways to go wrong: stale facts come back as gospel, and you cannot always see what it pulled in.

Just re-explaining. Some people re-explain from scratch every time and swear the friction keeps them honest about what the agent actually needs to know.

## Where I have landed

A short project file for the stable stuff, conventions, architecture, the "do not touch, see incident" notes that actually break things if ignored, and then re-explaining the task-specific context fresh each time. That second part changes too fast to keep in a file without it rotting. So the project file is the part I trust, and the per-task context is the part I gave up trying to persist.

But I flip on this every few weeks, and the memory-server people make a real case that I am just doing by hand what a good retrieval layer would do better and without my forgetting.

## So, honestly

1. What is actually in your setup right now, concretely? A file, a server, a ritual you run at the start of every session?
2. Does it actually help, or does it just feel productive while the agent quietly ignores half of it?

I ask the second one because I caught my own project file sitting three weeks out of date while I confidently assumed the agent was following it. The gap between "I wrote it down" and "the agent used it" is where I keep getting surprised, and I suspect I am not the only one.
