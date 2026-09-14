<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/13 post 2/3. FORMAT: practical/tool (real pre-commit hook setup). Ties to repo-lockdown but distinct: concrete hook config.
- Standard, verifiable tooling (gitleaks, pre-commit framework). Real config.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "The pre-commit hook that stops a secret from ever reaching your repo"
published: false
description: "An AI agent that reads and writes files will eventually stage a key or a token. A ten-minute pre-commit hook catches it at the last safe moment, before it becomes a commit you can't unpublish."
tags: security, git, programming, ai
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-13-precommit-hook-secrets/cover.png
---

The worst place to find an API key is in your git history, because once it is committed and pushed it is effectively public forever, even if you delete it in the next commit. Rotating the key is then the only real fix. This gets more likely, not less, once an AI agent is reading and writing files in your repo, because the agent is a fast, tireless, and occasionally careless author. A pre-commit hook is the last safe moment to catch a secret, and it takes about ten minutes to set up.

## The last line of defense, before the point of no return

A pre-commit hook runs on your machine after you `git add` and before the commit is created. That timing is the whole point: the secret is staged but not yet in history, so blocking the commit means the secret never becomes permanent. Compare that to catching it in CI, which fires after the push, when the key is already in a remote and already burned. Local, pre-commit, is the only spot where prevention is still cheap.

## The setup

Use the `pre-commit` framework and a secret scanner. Two files and one install command.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
```

```bash
pip install pre-commit        # or brew install pre-commit
pre-commit install            # wires it into .git/hooks
```

That is the baseline. From now on every commit is scanned for the shapes of known secrets, AWS keys, tokens, private keys, high-entropy strings, and a match blocks the commit with the file and line called out. The agent stages a `.env` with a real key, the commit fails, you catch it while it is still local and fixable.

## Do not rely on the scanner alone

A scanner catches the secrets that match a pattern. Back it with the boring habit that catches the rest: keep secrets out of the tree in the first place. `.env` in `.gitignore`, real values in the environment, and a committed `.env.example` with the keys blanked so the shape is documented without the values. The scanner is the safety net for when that discipline slips, not a replacement for it.

You can add cheap project-specific checks to the same hook while you are there. A grep that rejects a staged `TODO: remove before commit`, a check that no file over a certain size is being added, a block on committing to `main` directly. Each is a few lines and each closes a hole an agent will eventually find.

```yaml
  - repo: local
    hooks:
      - id: no-direct-main-commit
        name: block direct commits to main
        entry: bash -c '[ "$(git symbolic-ref --short HEAD)" != "main" ]'
        language: system
        pass_filenames: false
```

## Why this matters more with agents in the loop

A human author commits a few times an hour and roughly knows what is in each change. An agent can generate and stage dozens of files in a burst, and it does not feel the flush of dread you feel when you realize a config with a live key just went in. The hook does not get tired and does not move faster than its own judgment, so it is exactly the check you want standing between an automated author and your history. Set it once and it protects every commit after, whoever or whatever wrote it.

Ten minutes, two files, one install. The payoff is that the single most expensive mistake, a live credential in public git history, stops being possible on your machine instead of being something you clean up after.

If you run a pre-commit setup with a check I have not thought of, I want to see it, because the good ones are all learned from a near-miss someone would rather not repeat.
