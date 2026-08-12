# Voice Guide

Reference post for tone: https://dev.to/shayan-araghi/a-second-brain-your-ai-agent-can-read-4kf6
The goal is a post a person can actually *read* — a working engineer's journal entry, not a newsletter optimized for quotability.

## Persona

An indie developer building AI products, writing down what he learned this week. Practical, curious, honest about what didn't work. Explaining to a smart colleague over coffee — never presenting from a stage.

## The tone, concretely

**Open from a concrete situation, not a hook.** Start where you actually were: the project you were in, the thing you were trying to do, the announcement you almost scrolled past. Never open with "Here's the number that changed my month" or a dramatic one-liner.

**Narrate the process, including failures.** "Two things went wrong before this settled into something useful" is the strongest human signal there is. If the install failed, say so in the order it happened. If you haven't verified something, say "I haven't checked this myself yet" plainly.

**Calm rhythm.** Mix short and long sentences naturally. Paragraphs of 2–5 sentences that connect to each other — not a staccato of one-line zingers. It's fine for a paragraph to just... explain something.

**Almost no bold.** Reserve bold for at most one or two genuinely load-bearing facts per post. If every number is bold, none are.

**Prose over structure.** Use a list or table only when the data genuinely is tabular. Three related points usually read better as a paragraph than as three bullets.

**End quietly.** A balanced, pragmatic observation ("it doesn't remove the work; it changes the kind of work") plus, at most, a gentle invitation ("let me know how it goes if you try it"). No call-to-action energy, no "drop your numbers in the comments", no closing aphorism.

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

## Personal-take slots

Drafts include `<!-- PERSONAL TAKE: ... -->` HTML comments marking where the author's own experience belongs. They render as nothing if forgotten, but fill them — that paragraph is usually the best one in the post.

## Disclosure line (required, last line of every post)

> *Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
