<!--
REVIEW NOTES (delete before publishing)
- COVER IMAGE: assets/2026-08-21-owasp.png
- Optional chart: ranking movement (Excessive Agency 6→3, Improper Output Handling 5→10). assets/2026-08-21-owasp-chart.png
- Facts (research/2026-08-19-topic-scan.md): published Aug 4; #1 Prompt Injection unchanged, #2 Sensitive Info Disclosure, Excessive Agency 6→3, System Prompt Leakage renamed Hidden Context Exposure, Improper Output Handling 5→10; first incident-weighted (75% vote + 25% from 6,639 real incidents); Appendix A maps to enterprise standards.
- Security post: practical, no scaremongering.
-->

---
title: "The OWASP LLM Top 10 just moved 'Excessive Agency' to #3, and it's the ranking that should worry you"
published: false
description: "The 2026 list is the first weighted by real incidents. Prompt injection still leads — but the risk climbing fastest is the one you introduce every time you give an agent a tool."
tags: security, ai, agents, webdev
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-21-owasp.png
---

OWASP published the 2026 GenAI LLM Top 10 this month, and one number moved enough to be worth a post: Excessive Agency jumped from sixth place to third. Prompt injection is still #1 and probably always will be, sensitive information disclosure holds #2 — but the risk climbing the chart is the one you create yourself, on purpose, every time you hand an agent a tool.

There's also a methodology change that makes this list matter more than previous editions.

## This one is graded on reality

Past OWASP LLM lists were essentially expert consensus — smart people voting on what felt most dangerous. The 2026 edition keeps the vote at 75% of the weight but adds 25% from 6,639 real-world incidents pulled from public vulnerability and AI-harm databases.

That shift is why the movement is worth reading as signal rather than opinion. Excessive Agency didn't climb because a committee got more worried about it in the abstract. It climbed because it's showing up in the incident data — actual systems, causing actual harm, because an agent was allowed to do more than it should have.

## What "Excessive Agency" actually means

The name is vaguer than the problem. Excessive Agency is what happens when an LLM can *take actions* — call APIs, run code, send emails, move money — and the guardrails on those actions are weaker than the ways the model can be talked into misusing them. It's the compound risk of two things we're doing simultaneously: making models easy to manipulate (prompt injection, #1) and giving them real hands (tools, autonomy).

Put those together and the failure mode writes itself. A prompt-injected model with no tools produces bad text. A prompt-injected model with your production database credentials and a `send_email` tool produces an incident. The industry spent the last two years racing to give agents more capabilities, and the incident data is now catching up to what that costs when the model underneath can be fooled — which OWASP bluntly says it can, and always will be.

The rest of the reshuffle tells the same story from other angles. System Prompt Leakage got renamed Hidden Context Exposure, widening it to all the sensitive context now flowing through these systems. Improper Output Handling fell from fifth to tenth — not because it stopped mattering, but because the field's attention moved from "the model said something bad" to "the model *did* something bad."

## What I'd take back to my own code

Three practical things, none of them exotic.

Scope tools like you scope database permissions. An agent should have the narrowest set of actions its task requires, not the full toolbox because it was convenient. If a read-only task has a write-capable tool in reach, that's Excessive Agency waiting for a bad prompt.

Assume the model will be fooled, and put the real guardrail after it, not inside it. Prompt injection is #1 for a reason — you will not prompt your way to safety. The enforceable boundary is in the code that executes the tool call: permission checks, confirmation gates on irreversible actions, spend limits. Treat model output as an untrusted request to your action layer, because that's what it is.

Inventory what your agents can actually do. Most teams can list their agents' capabilities far faster than they can list the *combinations* those capabilities enable. The V8 of agent security is the interaction between tools, and that's exactly the surface the incident data is lighting up.

The 2026 list has an Appendix A mapping each risk to established enterprise security standards, which is a quietly big deal if you need to justify this work to a security team in their language. Worth a look even if you only skim the top three.

If your team has already tightened tool scoping after a close call, I'd like to hear what triggered it — those stories are more useful than any ranking.
