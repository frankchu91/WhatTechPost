<!--
REVIEW NOTES (delete before publishing)
- Core fact (Bedrock Agents renamed "Bedrock Agents Classic", closed to new customers as of July 30, 2026) comes from one aggregator source — VERIFY against AWS's own docs/announcement page before publishing. If AWS framing differs materially, adjust the opening.
- The general argument doesn't depend on Bedrock specifics, but the hook does.
-->

---
title: "Your agent framework will be renamed 'Classic' sooner than you think"
published: false
description: "Amazon quietly closed Bedrock Agents to new customers. A short field guide to building on agent platforms while the ground is still moving."
tags: aws, ai, architecture, agents
---

Amazon renamed Bedrock Agents to "Bedrock Agents Classic" at the end of July and closed it to new customers. If you've spent any time around AWS, you know what the word Classic means in that sentence: it's the word that appears on a service's tombstone a few years before the funeral.

I don't have inside knowledge of what replaces it, and existing customers presumably keep running for a long transition window — that's how these sunsets go. But the rename is worth a post, because it's the clearest signal yet of something everyone building agents has quietly suspected: the agent-platform layer is nowhere near settled, and the vendors know it.

## Why agent platforms keep churning

Think about what an agent platform circa 2024–25 had to bet on: how tools get defined, how orchestration works, how memory persists, how humans approve actions. Every one of those bets has since been re-litigated. Tool definitions converged on MCP rather than per-platform schemas. Orchestration is drifting from vendor workflow-graphs toward plain code — that's the entire NOOA thesis. Model routing is becoming its own layer. The platforms built on the old bets aren't badly engineered; they're built on assumptions the field discarded in eighteen months.

That's the general mechanism, and it isn't done.