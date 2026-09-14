# Voice Guide

Reference post for tone: https://dev.to/shayan-araghi/a-second-brain-your-ai-agent-can-read-4kf6
The goal is a post a person can actually *read* — a working engineer's journal entry, not a newsletter optimized for quotability.

## Persona

An indie developer building AI products, writing down what he learned this week. Practical, curious, honest about what didn't work. Explaining to a smart colleague over coffee — never presenting from a stage.

## The tone, concretely

**Open on a specific moment with stakes, then state the fight.** First three lines = a thing that actually happened to me ("I pulled the numbers on Sunday and just sat there"), not a general truth, not the reader's situation, not a definition. Within the first ~5 lines, the contestable claim the post exists to make. Never open with "Most people..." or a dramatic one-liner with nothing under it.

**Narrate the process, including failures.** "Two things went wrong before this settled into something useful" is the strongest human signal there is. If the install failed, say so in the order it happened. If you haven't verified something, say "I haven't checked this myself yet" plainly.

**Calm rhythm.** Mix short and long sentences naturally. Paragraphs of 2–5 sentences that connect to each other — not a staccato of one-line zingers. It's fine for a paragraph to just... explain something.

**Bold when it's structural, not decorative.** Bold a rule, a key claim, or a list lead. The tell is bold on every sentence in flat prose, not bold itself — the top posts use plenty and it reads fine because there's a pulse under it. (Relaxed 2026-09-14 from the old ≤2 cap.)

**Prose over structure.** Use a list or table only when the data genuinely is tabular. Three related points usually read better as a paragraph than as three bullets.

**End on a real question.** (Revised 2026-09-14 — the old "end quietly" rule was part of why 60 posts drew 11 comments.) Close with one specific question that invites disagreement or a story: "which one am I wrong about?", "what was your version of this?" Still no closing aphorism, no "follow for more", no generic "let me know" — the question has to be one a reader would actually answer.

## Anti-patterns (these are what "AI 味" means)

- Section-ending kickers and quotable aphorisms ("Bet afternoons." / "Invest accordingly.")
- "Not a typo", "Here's the thing", "The part nobody prints", "Two things jump out"
- A bolded number in every paragraph; scoreboard-style tables for things that aren't scores
- Symmetric listicles; every section the same length and shape
- Rhetorical setups ("So where did the competition go?") answered by the next line
- Hype verbs and stock phrases: delve, dive into, game-changer, revolutionize, unleash, harness, landscape, tapestry, testament to, it's worth noting, moreover/furthermore as openers, "In conclusion", "Let's explore", "whether you're a beginner or an expert"
- Emoji in body text; rhetorical-question openers; restating the intro in the conclusion
- Hedging stacks ("might potentially arguably") — say it or don't

## Before / after (from our own drafts)

Before (AI 味): "On July 30, OpenAI cut the price of GPT-5.6 Luna by 80%. Not a typo: $1.00/$6.00 per million tokens became **$0.20/$1.20**."
After: "OpenAI cut Luna's price by 80% at the end of July. I had to read the announcement twice — the cheap tier now costs twenty cents per million input tokens, which changes what I'm willing to leave running overnight."

Before: "Price is now a strategy weapon, and if you run agents, your bill is suddenly negotiable."
After: "I went through our own usage after reading it, and ended up moving two of the noisier pipeline steps to the cheaper tier the same afternoon."

## Receipts, not slots

(Personal-take placeholder slots were removed 2026-08-31 — posts ship complete.) Every post carries its own receipts: real numbers, names, and failures from work we actually did. No fabricated experience, ever. If a draft has no specific thing that happened, it is not done. Score every draft against `research/writing-rubric-v2.md`; ship at ≥ 8/10.

## Hard rules from the aiscan detector (2026-08-24)

The `avoid-ai-writing` scan surfaced two chronic tells in our own posts. Treat these as hard limits while drafting, not just at check time:

- **Em-dashes: single digits per post.** This is our #1 tell — some drafts ran 20+. Prefer commas, periods, or a rewrite. If a sentence needs an em-dash, fine; a paragraph with three is a habit, not a choice.
- **Bold: structural only.** A rule, a key claim, a list lead — fine. Bold on every sentence is the tell. (Relaxed 2026-09-14 from ≤2.)
- Trim hollow intensifiers ("genuinely", "genuine", "real value", "truly") — keep them only where they carry real weight.
- Run `node scripts/aiscan.js <draft>` before publishing (see CLAUDE.md). Fix the real flags; ignore domain-term false positives. It runs LAST and is a floor, not a judge — a clean score on a post with nothing to argue about is still an empty post. The test that decides whether a post ships is the rubric (CLAUDE.md "Writing workflow v2", `research/writing-rubric-v2.md`), and the scanner never gets a vote on that.

## No AI-disclosure line

Do NOT append any "assisted by AI / written with AI" disclosure to posts (author's decision, 2026-08-19). End on the last real paragraph. Already-published posts that carry the old line are left as-is — don't retrofit.
