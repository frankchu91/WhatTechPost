<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 3 (9/12), post 3/3. FORMAT: discussion (提问式), discuss tag. Short (~470w). Ends on a real question.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png (OPINION).
-->

---
title: "Do you still read the docs, or do you just ask the model now?"
published: false
description: "I catch myself asking the model instead of opening the official docs. Sometimes it's faster. Sometimes it confidently invents an API that doesn't exist. Where's your line?"
tags: discuss, ai, productivity, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-12-docs-vs-ask-discussion/cover.png
---

I noticed a habit in myself recently that I am not sure how to feel about. When I hit a question about a library or an API, my first move is no longer to open the docs. It is to ask the model. And most of the time that is faster and fine. Some of the time it confidently hands me a method that does not exist, an argument that was renamed two versions ago, or a pattern that was good advice in 2023 and is wrong now.

So I want to know where other people have drawn this line, because I do not think I have drawn mine consciously.

The case for asking the model is real. It is faster, it answers the exact question instead of making you find it, and for stable, well-trodden things it is almost always right. Asking "how do I flatten a list in Python" and reading three paragraphs of docs would be silly.

The case for the docs is also real, and it is mostly about the failure mode. The model's wrong answers do not look wrong. They look exactly as confident as the right ones, which means the cost of a mistake is not "I got no answer," it is "I built on a plausible invention and found out later." For anything new, anything niche, anything where the version matters, the docs are the only source that cannot hallucinate.

Where I am landing, unevenly, is something like: ask the model for the shape of the answer and the direction, then confirm against the docs anything I am going to depend on, especially if it is a newer API or a security-relevant detail. The model is a fast index and a poor source of truth, and treating it as the first but never the last word has saved me more than once.

But I break my own rule constantly, usually when I am moving fast and the answer looks right.

So, honestly:

1. What is your actual split now? Docs first, model first, model-then-verify, something else?
2. When has the model's confident answer burned you, and did it change your habit, or did you just sigh and keep asking?

I am after the specific cases, the time the invented API cost you an hour, because those are the ones that actually calibrate where the line should be, and most of us are drawing it by feel.
