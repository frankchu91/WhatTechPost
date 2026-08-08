# dev.to AI Content Project

Personal tech-brand blog on dev.to. Author persona: **indie builder** — a developer actively building AI products, writing about the latest AI news from a "what does this mean for builders" perspective.

## Cadence & Workflow

- One post every 3 days (scheduled pipeline drafts it; human reviews and publishes manually).
- Pipeline: scan news (last 3 days) → pick 1 topic → research primary sources + run real code where possible → draft in English → save to `drafts/` → notify.
- Human review gate: the user reviews every draft, adds personal takes, publishes by copy-pasting into dev.to, then tells Claude to archive to `published/`.

## Content Rules (anti-AI-dump quality bar)

Every post MUST have:
1. One original opinion/stance — never a paraphrase of the official announcement.
2. At least one piece of verified evidence: code actually run, numbers actually checked, or a primary source read end-to-end (notes in `research/`).
3. First-person builder voice per `VOICE.md`.
4. An AI-assistance disclosure line at the end (dev.to policy).

If a draft can't meet the bar, skip the cycle rather than publish filler.

Content mix: ~2/3 engineer's-lens news analysis (800–1500 words), ~1/3 deep technical breakdowns. Never plain news roundups.

## Structure

- `drafts/YYYY-MM-DD-slug.md` — pending review, with dev.to front matter (title, published: false, tags, canonical_url empty).
- `published/` — archived published posts + URL + post-mortem notes.
- `research/YYYY-MM-DD-slug.md` — sources and test outputs backing each draft.
- `TOPICS.md` — candidate topic pool and used-topic log (check before picking to avoid repeats).
- `VOICE.md` — voice guide and banned-phrase list. Follow it strictly.

## Publishing via API

`scripts/publish.py` posts a draft to dev.to (Forem API). Requires `DEVTO_API_KEY` in `.env` (gitignored) — generate at dev.to Settings → Extensions.

- `python3 scripts/publish.py drafts/X.md` → creates a **draft** on dev.to (safe default)
- `python3 scripts/publish.py drafts/X.md --publish` → publishes live
- `--dry-run` → prints payload, no API call

The script strips the leading REVIEW-NOTES comment and refuses to run while a `[PERSONAL TAKE]` placeholder remains — that gate is intentional, do not bypass it.

## dev.to Conventions

- Tags: 3–4, always include high-traffic ones (#ai, #llm, #programming, #machinelearning as fits) + one precise niche tag.
- Titles: concrete benefit + concrete audience; no clickbait, no "🚀 Game-Changer" style.
- Front matter template:

```yaml
---
title: "..."
published: false
description: "..."
tags: ai, llm, programming
---
```
