<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-27-buzz.png
- Facts (research/2026-08-27-topic-scan.md): Block's Buzz, open-source workspace (chat + AI agents + Git), Nostr relay in Rust, Apache 2.0, github.com/block/buzz; every agent gets its own cryptographic identity, permissions, audit trail; ~22.9k stars by late Aug (launched Jul 21). Jack Dorsey / Block.
- Written to pass aiscan. Re-run node scripts/aiscan.js before publishing.
- No AI-disclosure line (policy).
-->

---
title: "Jack Dorsey's Buzz gives every AI agent its own login. That's the idea worth copying"
published: false
description: "Block open-sourced a Slack-plus-GitHub workspace where agents get the same cryptographic identity, permissions, and audit trail as humans. The feature matters more than the app."
tags: ai, agents, opensource, security
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-27-buzz.png
---

Block open-sourced a workspace called Buzz last month, and the pitch on paper is "quit Slack and GitHub, use one app." Team chat, AI agents, and Git hosting in a single interface, built on Nostr, written in Rust, Apache 2.0. It cleared sixteen thousand GitHub stars within days and kept climbing through August. The app itself is interesting. The design decision underneath it is the part I would steal.

In Buzz, every AI agent gets the same cryptographic identity, permissions, and audit trail you would give a human teammate. Not a shared bot token. Its own login.

## Why "its own login" is the whole thing

Think about how agents authenticate in most systems today. You create one service account, hand it an API key, and every agent action runs as that faceless account. When something goes wrong, and with autonomous agents it will, the audit log says the service account did it. Which agent? Acting for which user? On whose instruction? The log shrugs.

Buzz treats an agent the way a well-run company treats a contractor. It gets its own identity, a scoped set of permissions, and every action it takes is attributable to it specifically. If an agent deletes the wrong repo or posts something it should not have, you can see exactly which agent, running for which person, did it. That is the difference between an incident you can investigate and one you can only apologize for.

This is the same problem the Model Context Protocol roadmap just put near the top of its list under "agent identity and delegation." Buzz is one team's answer to it, shipped and running, instead of a spec. When two independent efforts land on the same idea in the same month, the idea is usually the real thing.

## The security story is not optional anymore

I keep coming back to a pattern from the OWASP LLM Top 10, where Excessive Agency climbed to number three: the danger with agents is rarely the model saying something wrong, it is the model doing something wrong through the access you gave it. Shared credentials make that worse in a specific way. When every agent runs as the same account, you cannot give one agent narrow permissions and another broad ones, and you cannot revoke a single misbehaving agent without breaking all of them.

Per-agent identity fixes the whole class. Scope each agent to exactly what its job needs. Revoke one without touching the rest. Read an audit trail that names names. None of that is exotic; it is how we already handle human accounts and service principals. Buzz's contribution is insisting that agents are not a special exception to identity, they are just a new kind of account, and should be modeled like one from the start.

## What to take from it even if you never touch Buzz

Most teams will not switch off Slack and GitHub this year, and that is fine, because the app is not the lesson. The lesson is the question to ask about your own system: when an agent acts, can you tell which agent, for whom, with what permissions, and can you turn just that one off?

If the answer is "everything runs as one bot account," you have the agent version of a shared root password, and you have it right as agents start doing real, irreversible work. You do not need Buzz to fix that. You need per-agent identities, scoped permissions, and an audit log that attributes actions to the specific agent. Build it now, while your agents are few and the blast radius is small, because retrofitting identity after you have fifty agents sharing one key is the kind of project nobody volunteers for.

Buzz is worth a look on its own terms, especially if the Slack-and-GitHub sprawl grates on you. But the reason I am writing about it is narrower and more portable than the app: agents are teammates now, so give them the accounts you would give a teammate.

If you have already set up per-agent identity in a real system, I would like to hear how you scoped it, because the how is where this gets hard.
