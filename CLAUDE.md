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

## AI-writing check (mandatory pre-publish step, added 2026-08-24)

Every draft must pass the AI-writing scan before it publishes:

```
node scripts/aiscan.js drafts/<file>.md
```

It runs the installed `avoid-ai-writing` detector and prints a score + flagged tells with a PASS / REVIEW verdict (exit 1 = REVIEW).

- **Score > 2 (REVIEW): fix and re-scan before publishing.** Don't publish a REVIEW draft.
- **Always fix the real, consistent tells**, even on a PASS: em-dash overuse (keep to single digits per post) and bold overuse (≤2 bold phrases per post). These are our two chronic habits; the scan catches them every time.
- **Use judgment on false positives** — it flags domain terms ("harness", "leverage-as-a-noun") and sometimes legitimate emphasis ("genuine"). Fix real ones; don't chase the number by mangling correct writing. The tool itself says: signal, not verdict.
- Run it after writing/rewriting and again after any edit. A rewrite to lower the score must not introduce factual drift.

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

Reference post the reader flagged as too dry: a long unbroken column of prose. Fix: give every post visual anchors. Images are generated as PNGs into the post's `drafts/` folder (colocated with its markdown) and referenced by raw URL; on publish the whole folder set moves to `published/` and is pushed (see Repo layout below).

Generators (HTML+CSS → headless Chrome screenshot, fully style-controlled):
- `scripts/make_cover.py --kicker --title --meta --accent --out drafts/<slug>.png` — branded 1000x420 cover. **Every post gets one.** Kicker signals type (HANDS-ON / TECH ANALYSIS / SECURITY / TREND / OPINION / PLATFORM). Accent = topic brand color (nvidia #76b900, aws #ff9900, cloudflare #f6821f, meta #0866ff, security #ef4444, default #38bdf8).
- `scripts/make_barchart.py --spec chart.json --out drafts/<slug>-chart.png` — grouped/single bar chart for any benchmark/price/perf numbers.

Per-post visual budget (aim for all that apply):
- 1 cover (always) · 1+ data chart or real screenshot when there are numbers · 2–3 dev.to rich cards · 1 pulled `> blockquote` from a primary source · code blocks with real config/output.

dev.to rich cards (pure markdown, zero hosting): `{% embed <news-url> %}` (link preview), `{% github owner/repo %}` (repo card), `{% link <your-devto-post-url> %}` (own-post card), `{% tweet %}`, `{% youtube %}`.

### Repo layout & image hosting (WhatTechPost is public) — one folder per post (2026-08-29)

**Each post gets its OWN folder holding its markdown + its images.**

```
drafts/2026-08-29-i-built-coding-agent-router/   ← one post = one folder
   index.md         ← the article (always index.md)
   cover.png        ← cover image
   receipt.png      ← any inline charts/cards, short names
```

- `drafts/<slug>/` — **gitignored, local only.** One folder per unpublished post: `index.md` + its PNGs. Unpublished work never hits the public repo.
- `published/<slug>/` — **tracked and pushed.** Same folder moved here on publish; the public raw-URL source going forward.
- `assets/` — **FROZEN / legacy.** Flat images for posts published before 2026-08-29. Those live posts hot-link `…/main/assets/<file>.png`, so do NOT move, rename, or delete anything here or their inline images break. New posts do not use it. (Pre-8/29 published markdown also stays flat in `published/*.md`; only new posts use the per-folder layout.)
- New-post image URLs: `https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/<slug>/<img>.png` (cover via `cover_image:` front matter, charts as inline `![]()`). 404s until the folder is moved to `published/` and pushed — which is exactly the publish step.
- Generate a draft's images straight into its folder: `make_cover.py --out drafts/<slug>/cover.png`, `make_barchart.py --out drafts/<slug>/<name>-chart.png`.

**Publish flow (no manual image handling):**
1. Move the whole folder: `drafts/<slug>/ → published/<slug>/`.
2. `git add -A && commit && push` — now the `…/main/published/<slug>/<img>.png` raw URLs resolve.
3. Publish via API: `python3 scripts/publish.py published/<slug>/index.md --publish`. Cover and inline images load from the raw URLs automatically.
4. Before publishing: strip REVIEW NOTES, fill any `[[PERSONAL TAKE]]`, and `node scripts/aiscan.js published/<slug>/index.md` must reach PASS.

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
