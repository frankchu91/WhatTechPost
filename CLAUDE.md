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

(No AI-assistance disclosure line — removed 2026-08-19 by the author's decision. Do NOT add one to new posts. Already-published posts keep whatever they shipped with; don't retrofit.)

If a draft can't meet the bar, skip the cycle rather than publish filler.

Content mix (revised 2026-08-13): two kinds of posts, both welcome —
1. **Hands-on** (the signature): install/build/benchmark/breakage with real numbers, code, and errors from this machine (M2 Pro, 32GB). Scripts in `scripts/`, raw results in `research/data/`, linked from the post.
2. **Tech analysis**: news interpretation, explainers, trend pieces — no bench run required, but facts must be first-hand verified (read the model card / license / repo / discussion yourself, quote precisely) and the post needs an original stance.

Hands-on when the story benefits from it, analysis when speed or the topic calls for it. Never plain news roundups, never uncritical relays of vendor claims.

## Structure

- `drafts/YYYY-MM-DD-slug.md` — pending review, with dev.to front matter (title, published: false, tags, canonical_url empty).
- `published/` — archived published posts + URL + post-mortem notes.
- `research/YYYY-MM-DD-slug.md` — sources and test outputs backing each draft.
- `TOPICS.md` — candidate topic pool and used-topic log (check before picking to avoid repeats).
- `VOICE.md` — voice guide and banned-phrase list. Follow it strictly.

## Visual assets (every post — no walls of text)

Reference post the reader flagged as too dry: a long unbroken column of prose. Fix: give every post visual anchors. Assets are generated locally as PNGs into `assets/` and uploaded by the human in the dev.to editor (drag-drop → dev.to CDN; images are NOT hosted in the repo, so no public-repo dependency).

Generators (HTML+CSS → headless Chrome screenshot, fully style-controlled):
- `scripts/make_cover.py --kicker --title --meta --accent --out assets/<slug>.png` — branded 1000x420 cover. **Every post gets one.** Kicker signals type (HANDS-ON / TECH ANALYSIS / SECURITY / TREND / OPINION / PLATFORM). Accent = topic brand color (nvidia #76b900, aws #ff9900, cloudflare #f6821f, meta #0866ff, security #ef4444, default #38bdf8).
- `scripts/make_barchart.py --spec chart.json --out assets/<slug>-chart.png` — grouped/single bar chart for any benchmark/price/perf numbers.

Per-post visual budget (aim for all that apply):
- 1 cover (always) · 1+ data chart or real screenshot when there are numbers · 2–3 dev.to rich cards · 1 pulled `> blockquote` from a primary source · code blocks with real config/output.

dev.to rich cards (pure markdown, zero hosting): `{% embed <news-url> %}` (link preview), `{% github owner/repo %}` (repo card), `{% link <your-devto-post-url> %}` (own-post card), `{% tweet %}`, `{% youtube %}`.

### Repo layout & image hosting (WhatTechPost is public)

- `drafts/` and `drafts-assets/` are **gitignored — local only.** Unpublished work never hits the public repo.
- `published/` (markdown) and `assets/` (PNGs) are **tracked and pushed.** Only published posts' assets live in `assets/`.
- Draft markdown already references final image URLs: `https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/<file>.png` (cover via `cover_image:` front matter, charts as inline `![]()`). The URL 404s until the asset is moved to `assets/` and pushed — which is exactly the publish step.

**Publish flow (no manual image handling):**
1. Move the post: `git mv`-style — markdown `drafts/ → published/`, its PNGs `drafts-assets/ → assets/`.
2. `git add -A && commit && push` — now the raw URLs resolve.
3. Publish the markdown (paste into dev.to editor OR API `body_markdown`). Cover and inline images load from the raw URLs automatically; nothing to upload or delete.
4. Strip the REVIEW NOTES comment and fill any `[[PERSONAL TAKE]]` before publishing (the API script enforces the latter).

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
