# dev.to AI Blog Account — Design Spec (2026-08-07)

## Goal

Grow a high-quality personal tech brand on dev.to via AI-news posts every 3 days. Explicitly avoid "AI dump" content; every post must survive technical scrutiny in the comments.

## Decisions (approved in brainstorm)

- **Positioning**: engineer's-lens news analysis (~2/3 of posts) + deep technical breakdowns (~1/3). No news roundups.
- **Persona**: indie builder — developer building AI products, first-person voice (see `VOICE.md`).
- **Purpose**: personal tech brand (followers, authority).
- **Workflow**: Claude drafts end-to-end (topic scan → research → real tests → draft); user reviews ~10–15 min, adds personal takes, publishes manually by copy-paste into dev.to; Claude archives after publish.
- **Cadence driver**: scheduled task every 3 days generates a draft into `drafts/` and notifies the user.
- **Publishing**: manual for now (existing dev.to account, no API key configured). May add API publishing later.
- **Language**: English.

## Quality bar (hard gate per post)

1. One original opinion, not a paraphrase of the announcement.
2. Verified evidence: code actually run / numbers checked / primary sources read (kept in `research/`).
3. Voice rules and banned-phrase list in `VOICE.md`.
4. AI-assistance disclosure line (dev.to policy).
5. If the bar can't be met, skip the cycle.

## Repo layout

`CLAUDE.md` (ops manual) · `VOICE.md` (voice guide) · `TOPICS.md` (topic pool + used log) · `drafts/` · `published/` · `research/` · git-versioned.

## Cold start (first 2–3 weeks)

- Ride high-traffic tags (#ai #llm #programming) + one precise niche tag per post.
- Titles: concrete benefit + concrete audience.
- User spends ~5 min/day leaving substantive comments on adjacent dev.to posts.
- Reply to all comments within 24h of publishing.

## Out of scope (for now)

dev.to API auto-publish, cross-posting (Hashnode/Medium), analytics automation, cover-image generation pipeline.
