<!--
REVIEW NOTES (delete before publishing)
- COVER IMAGE (dev.to editor "Add a cover image"): assets/2026-08-15-tldv.png
- Facts from researcher bobdahacker's disclosure blog + Dark Reading/Netizen coverage: 181,874 meetings, 84,312 users, 35,003 domains, missing Firestore rule on the meetings collection, ~6-month unresolved disclosure. Verify current status before publishing (has tl;dv fixed it / responded since?) — search "tldv fix statement" that morning.
- Tone care: this is about a real company's security failure — stick to the researcher's published facts, no speculation beyond them.
-->

---
title: "181,874 meetings, one missing security rule: the tl;dv leak is an architecture lesson"
published: false
description: "An AI notetaker left its meetings collection readable by any signed-in user. The bug is mundane. What it says about the tools we wire into everything isn't."
tags: security, ai, saas, architecture
---

A security researcher known as bobdahacker published a disclosure this month about tl;dv, the AI notetaker that joins your Zoom, Meet, and Teams calls: 181,874 meeting records from 84,312 users across 35,003 domains were readable by any authenticated user. Not through some exotic exploit chain — through a missing Firestore security rule. By the researcher's account, some records included live calls a stranger could have joined, and the disclosure sat unresolved for around six months of follow-ups.

The bug itself is almost boring, which is why it's worth writing about.

## The mundane mechanics

tl;dv's client authenticates, exchanges a session credential for a Firebase token, and talks to Firestore directly — a completely standard serverless architecture. Per-tenant isolation in that architecture lives in security rules, collection by collection. Most of tl;dv's collections had correct rules. The `meetings` collection didn't, so any signed-in user could list every tenant's documents.

One missing rule. That's the entire vulnerability. Firestore's whole model concentrates authorization into declarative rules precisely so it can't be scattered across application code — but concentration cuts both ways: a single omission becomes a total, queryable breach with a valid token being the only requirement. If you build on Firestore or Supabase or any client-talks-to-database platform, "list documents from every collection as an ordinary signed-in user" belongs in your CI, not your incident retro. It's among the cheapest security tests that exists.

## The part specific to AI tools

Here's what makes this more than a generic SaaS breach story. An AI notetaker is not an app you use; it's an agent you *invite* — into board meetings, sales negotiations, standups, one-on-ones. Its entire value proposition is having access to everything and remembering all of it. Which means its blast radius isn't "user data" in the abstract; it's the verbatim content of conversations from 35,003 different organizations, indexed and transcribed for convenient exfiltration.

We're currently wiring AI tools into calendars, inboxes, codebases, and meetings at extraordinary speed, and the security conversation around them fixates on the model — prompt injection, jailbreaks, data in training sets. The tl;dv failure had nothing to do with AI at all. It was 2015-vintage access control on 2026-vintage data concentration. The model risks are real, but the boring risks got there first, and they scale with how much we've granted these tools access to — which is, increasingly, everything.

The six-month disclosure timeline deserves its own sentence: a researcher reporting "all your meetings are public" and following up repeatedly without resolution is a process failure as serious as the bug.

## What I'd actually do

Three things, none dramatic. When evaluating any AI tool that ingests sensitive material, ask where authorization is enforced — client-side rules, an API layer, row-level security — and whether they've had it tested; a company that can't answer crisply has answered. Prefer tools whose recording/retention you can scope: a notetaker that can't see a meeting can't leak it, and default-record-everything is a liability posture, not a feature. And inside your own org, treat "which agents have standing access to what" as an actual inventory, the way you'd track service accounts — because that's what these tools are.

None of this is anti-AI-tooling; I run an AI notetaker's output through half my workflow. It's a request for proportion: the tools with the deepest access are getting the shallowest scrutiny, and the tl;dv disclosure is what that looks like when someone finally checks.

If your team runs a vendor-security checklist for AI tools specifically, I'd genuinely like to see what's on it.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
