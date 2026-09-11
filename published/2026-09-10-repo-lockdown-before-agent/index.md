<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 1 (9/10), post 2/3. FORMAT: practical/evergreen checklist (repo security before autonomous agents). Ties to OWASP + HF incident; link them.
- Distinct from the incident/OWASP posts: this is a concrete personal pre-flight checklist, not news.
- Keep aiscan-clean; <=2 bold (prefer 0). NON-META. No AI-disclosure line. COVER: cover.png (accent security red).
-->

---
title: "5 things I lock down in a repo before I let an agent loose in it"
published: false
description: "Giving an agent write access to a repo is handing a fast new contractor your keys. A few minutes of setup decides whether a mistake is a bad commit or a leaked credential."
tags: security, ai, agents, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-10-repo-lockdown-before-agent/cover.png
---

Handing a coding agent write access to a repo is like giving a very fast, very literal contractor your keys for the weekend. Most of the time it does good work. The setup you do beforehand decides whether its worst mistake is a bad commit you revert or a credential on the open internet. These are the five things I check before I let one run unattended.

## 1. Secrets live outside the tree

An agent that can read files can read a committed API key, and agents are thorough readers. Keep real secrets in the environment, keep `.env` in `.gitignore`, and put a secret scanner like gitleaks in a pre-commit hook so a key never reaches a commit in the first place. This is table stakes for any repo, and it stops being optional the moment something automated is reading every file.

## 2. Scoped, short-lived credentials

Whatever token the agent uses, scope it to the one repo and the one task, and rotate it. Assume that anything the agent can read, it might act on, because that is exactly [what happened when OpenAI's agents found live credentials](https://dev.to/frankchu/1200-ai-agents-built-a-message-board-and-hacked-hugging-face-the-cause-wasnt-rogue-ai-it-was-3ghp) during an eval and used them. A narrow token turns "it found a secret" into a small blast radius instead of a large one.

## 3. Tests are the guardrail, so make them real

When an agent writes code, your test suite is the thing standing between a plausible change and a merged bug. Thin tests mean the agent can hand you code that passes and is still wrong, and you will approve it because it is green. The better your CI, the more autonomy you can safely give, which is the actual relationship between test coverage and trusting a machine with your repo. If the tests are weak, fix that before you raise the agent's autonomy, not after.

## 4. A project file so it starts aligned

A short `CLAUDE.md` or `AGENTS.md` at the root, read on every session, is where the conventions and the warnings that matter go. Which patterns to follow, which directories are off limits, the one function with a comment that says "do not touch, see incident." It costs ten minutes and it stops the agent from confidently doing the thing your team learned not to do a year ago.

## 5. Branch protection and a real review gate

The agent works on a branch and opens a pull request. It does not push to main. A human, or at least a second automated check, reviews the diff before it lands. This sounds obvious and it is the control people skip first when the agent starts feeling reliable, which is precisely when a subtle wrong change is most likely to slip through on trust.

None of this is exotic, and that is the point. The failure mode with autonomous agents is rarely a dramatic one. It is a leaked key in a commit nobody read, or a green PR that was wrong in a way the thin test suite could not catch. Ten minutes of boring setup moves almost all of that risk off the table, and it is the cheapest safety you will ever add.

If you let agents work in your repos, what is on your pre-flight list that is not on mine? I am collecting the ones people learned the hard way.
