<!--
REVIEW NOTES (delete before publishing)
- COVER: assets/2026-08-25-meta-muse.png (regenerated 8/24 — old cover had the wrong "modified license" claim)
- REWRITTEN 2026-08-24: original draft claimed Spark 1.2 weights come under a "modified Llama Community License" — verification found NO license has been published (Constellation Research: "no publication date and no published license"; businessmodelanalyst.com confirms; Zuckerberg only said "Soon we'll also release the weights"). Post reframed: the blank license line is the story.
- Verified facts: Muse Code beta Aug 5 (terminal agent, powered by Spark 1.2, $1.25/$4.25 per M tokens, discounted contributor tier = consent to training on your data); Muse Glimmer 30B Apache 2.0 (weights + quantized variants + drafter + perception encoder, no user gate / naming rule / AUP); Llama history: 700M-MAU threshold, "Built with Llama" naming rule, AUP.
- {% link %} card to Kimi K3 post — insert URL after Kimi publishes, placeholder KIMI_POST_URL.
- No AI-disclosure line (policy).
-->

---
title: "Meta says it'll open the weights for its flagship. The license line is still blank"
published: false
description: "Muse Code is in beta and Zuckerberg promised open weights for Muse Spark 1.2 — but no license has been published. After the Llama Community License years, that blank is the detail to watch."
tags: ai, llm, opensource, legal
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/assets/2026-08-25-meta-muse.png
---

Meta's superintelligence group shipped a coding agent this month — Muse Code, in beta, powered by a new coding-focused model called Muse Spark 1.2 — and Zuckerberg announced that the Spark 1.2 weights will be released too. I have a rule for these announcements, one I keep repeating in my open-weights posts: read the license before the model card. So before writing anything, I went looking for the Spark 1.2 license.

There isn't one. Not a restrictive one — none. No license text, no release date, just a promise:

> "Soon we'll also release the weights for Muse Spark 1.2, our latest foundation model." — Mark Zuckerberg

On a month where open weights keep reaching the actual frontier, a US lab promising to open its flagship is real news. But what that promise is worth depends entirely on a document that doesn't exist yet, and I think that blank line is worth a post on its own.

{% link KIMI_POST_URL %}

## "Open weights" and "open license" are different claims

I keep coming back to this because the industry keeps blurring it: you can download a model's weights and still be sharply limited in what you're allowed to do with them. "Open weights" tells you the file is available. The license tells you whether you can build a business on it, and those are separate facts that marketing loves to merge.

Meta itself is the best illustration, from just this month. Muse Glimmer, its 30B model, shipped with weights on Hugging Face under Apache 2.0 — and it's the genuinely clean kind of open: the license covers the full-precision weights, the quantized variants, even the companion drafter and perception encoder, with no user threshold, no naming requirement, no acceptable-use policy Meta can lean on later. Credit where due; after years of Llama's bespoke terms, that's the most permissive release Meta has ever done.

Muse Spark 1.2 is the opposite case: a flagship, promised open, with zero published terms. One model in each hand — a clean license you can read today, and a blank you're being asked to get excited about.

## Why you can't just assume it'll match Glimmer

The tempting inference is "Glimmer got Apache 2.0, so Spark 1.2 will too." Meta's own history is the argument against it. The Llama Community License looked open from a distance and carried real strings up close: a 700-million-monthly-user threshold that flipped you into negotiating with Meta, a "Built with Llama" naming rule, an acceptable-use policy. Those terms lived on Meta's most strategically important models for years while the company called them open source.

And Meta has already shown it treats the license as a per-model product decision, not a company default — Glimmer permissive now, Llama restrictive then, Muse Spark fully proprietary and cloud-only when it launched in April. Usually the more commercially central the model, the tighter the terms, because the license is doing the monetization the download price isn't. Spark 1.2 is the flagship. That's exactly the model where I'd expect the terms to carry conditions, and exactly why I'm not calling it open until I can read them.

The same read-the-terms reflex applies one shelf over, by the way: Muse Code's pricing has a discounted "contributor tier," and the discount is paid for by consenting to have your data used for training. That's a fine trade to make knowingly. It's the *knowingly* that takes reading.

## The move, same as always

When the Spark 1.2 license does land, the questions to answer before building anything load-bearing on it are the same three as ever: can you use it commercially at your scale, is there a user or revenue threshold that flips you into "call us" territory, and can you fine-tune, redistribute, and ship the result. If the answers are clean, this is a genuinely big deal — a US frontier flagship in open circulation, and I'll happily say so. If they're not, you've learned the release is really a free tier with a ceiling, which is fine to use knowingly and painful to discover after you've built on it.

Either way, the weights being promised is the easy half. The license is the half that decides what they're worth to you, and right now that half hasn't been written — or at least hasn't been shown to us. I'd rather wait for the text than write the celebration first.

If the license drops and you read it before I do, I'd genuinely like to hear what's in it — especially anything that isn't in Glimmer's Apache 2.0.
