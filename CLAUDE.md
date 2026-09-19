# dev.to AI Content Project

Personal tech-brand blog on dev.to. Author persona: **indie builder** — a developer actively building AI products, writing about the latest AI news from a "what does this mean for builders" perspective.

## Meta content — allowed as of 2026-09-12 (author lifted the prior ban)

The prior hard ban on Meta/Muse content was **lifted by the author on 2026-09-12**; the author explicitly decided Meta employee policy is not a blocker and asked to write Muse posts. Meta/Muse content is now permitted.

Residual guardrails (the only limits that remain): write only about **publicly available** Meta features and the author's own first-hand user experience. Do NOT publish anything confidential, internal, unreleased, or non-public about Meta. When in doubt on whether a detail is public, leave it out. (The author owns the employer-policy judgment; Claude's job is just to keep internal/unreleased specifics out of public posts.)

## Cadence & Workflow (revised 2026-08-31 — two posts/day, split by purpose)

Two posts a day, each with a different job. This replaced the "news-only" run after real dev.to top-post data (pulled 2026-08-31) showed straight news relays get almost no reads here — dev.to is a community, not a news feed. What gets read: discussion posts that ask the reader something, practical/evergreen craft, and "I built/tested X" hands-on. Almost no pure AI-news relays chart.

1. **Daily AI news digest — "Today in AI" — 1/day.** A short, scannable post that tells developers the day's big AI news, plainly. NOT a deep single-topic piece: a clear 3–5 item digest of what actually happened, each item one or two sentences plus a one-line "why a builder should care." Fast read (3–5 min). Still first-hand verified (no vendor-claim relays), still non-Meta. Its stance lives in what it selects and the per-item takes, not in a single thesis.
2. **One depth post — 1/day.** This is the piece that earns reads and follows. Rotate among:
   - **Hands-on** (the signature): "I built / I tested / I benchmarked X" with real numbers, code, and errors from this machine (M2 Pro, 32GB). Lean into it — this format charts on dev.to.
   - **Practical / evergreen** (priority format now): listicle, tutorial, tips, debugging war story. Searchable, skill-building, beginner-friendly. **Best source = our own work: real tools we built and real bugs/gotchas hit while building (the dev.to pipeline, the scripts, the router, the agents).** First-hand "here's the wall I hit and the fix" from this repo's own building is the most authentic material we have and needs no user input to be real.
   - **Discussion (提问式)**: a short post (2–4 min, `discuss` tag) that leads with the reader's situation and ends on one sharp question. Built for comments, not just reactions.

**Framing rule (the core lesson, 2026-08-31):** frame every post around the reader's work, not the news. "What does this change about how YOU build" beats "Company X did Y." Same-topic data showed the discussion-framed version out-engaged the news-framed one ~30x on comments. See [[writing-lessons-openings-distribution]].

- Pipeline: for the digest, scan the last 24h → gather + verify 3–5 items. For depth, scan the last 3 days → pick 1 topic → research primary sources / run real code. Draft in English → aiscan PASS → save to a per-post folder in `drafts/` → notify.
- **Fully streamlined (2026-08-31): zero required input from the user.** Every post must be written complete and publish-ready — NO `[PERSONAL TAKE]` slots, no placeholders, nothing the user has to fill or paste. Do not build posts that depend on the user contributing a personal anecdote. Claude writes the whole thing in the builder voice, runs aiscan to PASS, and generates the cover. **Publish gate (revised 2026-09-08): Claude does NOT auto-publish. Prepare the complete draft, then stop and wait for the user's explicit go ("发" / "publish") before moving the folder, pushing, and posting via the API.** The user still never writes or pastes anything; the only thing required from them is the green light to publish.

## Writing workflow v2 (2026-09-14) — the dev.to test

Built after real data: 60 posts → 690 views / 3 reactions / 6 followers, versus top posts at 100–186 reactions. Craft was not the variable; reads did not correlate with effort. Full rubric with scoring: `research/writing-rubric-v2.md`. Every draft is scored 0–10 before it is called done; ship at ≥ 8, rewrite below.

**Order of operations (do these in this order, not the reverse):**
1. **Thesis first.** Write the one line someone would argue with. If nobody could disagree, there is no post — pick another topic. "Correct, balanced advice" scores zero here.
2. **Open on a moment.** First 3 lines = a specific thing that happened to me, with stakes. Never "Most people…", never the reader's generic situation, never a definition.
3. **Receipts.** Real numbers, names, failures, from work we actually did. "690 views." "$0.12 vs $1.23." "Score 9, REVIEW." No fabricated experience, ever — every "I did X" must be something this repo/work really did.
4. **One human beat.** Self-deprecation, a flash of feeling, an aside. Vary sentence length. Do not sand every sentence to the same weight — that is how "not-machine" became "not-anyone."
5. **Punch title.** One clause, a claim or a question, ~10 words. Not "Title. Subclause that explains."
6. **End on a real question** that invites disagreement or a story. Never "let me know / follow for more."
7. **Scanner last.** aiscan as a floor, after the above, and it gets no vote on whether the post is worth publishing.

**Daily mix (author's rule, TIGHTENED AGAIN 2026-09-14):** 3 posts/day; **at least TWO of the three must be real hardcore technical posts — actual code, actual artifacts, actual things we built or found — not prose about technique.**

**Measured 2026-09-19 — topic is NOT the variable, reach is.** After 22 posts on the v2 workflow: self-referential posts about our own tooling averaged 7.4 views, reader-shared-problem posts averaged 7.1. No meaningful difference; every v2 post sits in a 0–39 noise band. An earlier read of this data ("self-referential posts are closed to readers") was drawn from the single top post and was wrong — the same one-sample mistake the linter-probe post is about. Do not re-litigate topic selection from a handful of view counts. The binding constraint is still 6 followers, and only distribution moves it: reply to every comment, comment with a real opinion on other people's posts, follow people in the lane.

**Hardcore posts must be self-verified, not recalled.** Every number, behavior, and claim in a technical post has to be measured or dug out in-session on this machine before it is written: run the probe, time the thing, diff the output, read the primary source. Then audit your own result — a measurement can be confidently wrong (a one-word test document once made me conclude the detector was density-based; re-running at realistic length gave the opposite answer). If a claim in a draft cannot be traced to something actually run today, cut it or go run it.

This is a hard gate, not a preference. It exists because 9 of 10 consecutive published posts shipped with **zero code blocks**, including a "methodology" post, and the author called it out: 纯文字谁看. Enforce it mechanically:

```
node scripts/techcheck.js drafts/<slug>/index.md     # exit 1 = prose, not technical
```

Requires >= 2 language-tagged code blocks and >= 12 lines of real code (REVIEW NOTES comments are stripped first, so notes never count). **The technical post of the day must exit 0 on techcheck before it is considered done.** What counts as substance: real code from `scripts/` or the actual work, a real skill/config file with its frontmatter, real command output or an error message, a real schema or spec. What does not: pseudo-code invented for the post, a bulleted "approach," or a table of concepts.

The other two rotate across styles: story/field report, contrarian opinion, industry news + stance, discussion, listicle-with-stance, setup share, war story. Vary the style day to day; ten posts in one style is one post.

**Distribution is part of the workflow, not an afterthought.** Reads come from reach, not craft: reply to every comment we get, comment with an actual opinion on 3–5 relevant posts/day (drafted by Claude, pasted by the author), follow people in the lane, cross-post pointers elsewhere. A great post into six followers is a great post nobody sees.

## Workflow: `comment` (author says "comment" / "帮我找帖子" / "给我评论")

Find dev.to posts worth replying to and hand the author ready-to-paste comments.

```
python3 scripts/comment.py          # candidates, ranked by comment activity
python3 scripts/comment.py --read <url>   # full body + existing comments, to draft against
python3 scripts/comment.py --mine         # unanswered comments on OUR posts (do these first)
```

**Output contract — this is the whole format, and it is strict:**

```
<url>

<English comment>

<url>

<English comment>
```

URL, then the comment, repeated. **Nothing else.** No "why I picked this one," no ranking
commentary, no Chinese explanation around them, no strategy notes, no closing summary.
The author pastes these directly; anything else is noise they have to read past.

Rules for the comments themselves:
- Always read the post body first (`--read`). A comment written off a title reads as spam.
- Be specific to what the post actually says: quote or name the exact point being answered.
- Bring a real number or a real failure from our own work when it fits. Never invent one.
- End on a genuine question the author would want to answer.
- **No links to our own posts.** First contact with a link reads as self-promotion.
- Don't repeat a point an existing commenter already made (the `--read` output lists them).
- Skip DEV staff/meta threads ("What was your win this week") — generic prompts, no conversation.

There is still no API to post comments (Forem v1 exposes GET `/comments` only), and
auto-posting would trip dev.to's spam system. Claude drafts, the author pastes.

## Engagement (comments) — human-in-the-loop only

Comments drive dev.to growth as much as posts, but there is NO API to post comments (Forem v1 exposes GET `/comments` only; posting needs a logged-in browser session). Do NOT try to auto-post comments — inauthentic bulk commenting is exactly what dev.to's spam system ("the Shield") flags, and it risks the account. The supported workflow: the user browses posts, Claude drafts 3–5 genuine, specific comments (react to the actual content, add a real point, optionally ask a question), the user pastes them. Quality over volume; a comment that adds nothing reads as spam whether a human or a model wrote it.

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
- **Always fix the real, consistent tells**, even on a PASS: em-dash overuse (keep to single digits per post) and the chronic filler words (the swap-table set: the verb that means "use," hollow intensifiers, "load-bearing," "comprehensive," etc. — do not list them in a draft's comment; the scanner reads comments). Bold is allowed when it is structural (a rule, a key claim, a list lead); the real tell is bold on every sentence in otherwise flat prose. The scanner is the LAST check and a floor, never a judge of whether a post is worth publishing (see Writing workflow v2).
- **Use judgment on false positives** — it flags domain terms ("harness", "leverage-as-a-noun") and sometimes legitimate emphasis ("genuine"). Fix real ones; don't chase the number by mangling correct writing. The tool itself says: signal, not verdict.
- Run it after writing/rewriting and again after any edit. A rewrite to lower the score must not introduce factual drift.

If a draft can't meet the bar, skip the cycle rather than publish filler.

Content-mix note (the formats live in Cadence & Workflow above; this is the quality bar for each):
- **Daily digest**: verify every item first-hand (read the model card / license / repo / post yourself, quote precisely). Never an uncritical relay of vendor claims. Coverage + clarity + per-item builder takes.
- **Hands-on**: install/build/benchmark/breakage with real numbers, code, and errors from this machine (M2 Pro, 32GB). Scripts in `scripts/`, raw results in `research/data/`, linked from the post.
- **Practical / evergreen** and **discussion**: still need a real point of view and first-hand-correct facts; the discussion post's job is to open a conversation, so it ends on a genuine question, not a CTA cliché.

The single deep analysis-of-one-news-item post (our old default) is now the exception, not the daily habit — if a story is big enough to deserve its own deep piece, it becomes that day's depth post instead of the digest lead. Never plain news roundups with no builder angle.

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
4. Before publishing: strip REVIEW NOTES (publish.py does this) and `node scripts/aiscan.js published/<slug>/index.md` must reach PASS. No `[PERSONAL TAKE]` placeholders anymore — posts ship complete (see streamlined rule under Cadence).

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
