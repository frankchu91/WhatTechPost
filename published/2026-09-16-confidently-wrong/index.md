<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/16 non-technical 3/3. Style: discussion, lighter. The opening example is real: my own probe harness returned a confidently wrong answer on a one-word document today.
-->

---
title: "What's the dumbest thing your AI confidently got wrong this week?"
published: false
description: "The failure I've made peace with is 'I don't know.' The one that still gets me is the fluent, self-assured, completely wrong answer delivered with zero hesitation. Trade me this week's best."
tags: discuss, ai, productivity, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-16-confidently-wrong/cover.png
---

The AI failure I have made peace with is "I do not know." That is honest and I can work with it. The one that still gets me is the fluent, confident, completely wrong answer, delivered with precisely the same certainty as a correct one. No hedge, no tell, just a wrong thing said well.

Mine this week was not even the model. It was my own measurement.

I was testing a linter to find out how it scores text, so I fed it a single word and got a zero. Fed it the same word forty times and got a five. Clear conclusion: the scoring is density-based, one occurrence is free. I was about to write that down as fact when I noticed the input was one word long, which is not a small document, it is a degenerate one. Re-running with a realistic amount of text gave the opposite answer. The harness was correct the whole time. The input was the lie, and it sounded exactly as authoritative as the truth would have.

Which is the same shape as the model failures. Last month I asked about a library's API and got a method that does not exist, with plausible arguments, a realistic docstring, and a usage example. It looked more real than the real methods. I spent a few minutes debugging why it was not importing before I accepted that the whole thing had been invented.

That is the part worth sitting with. The wrong answers are not obviously wrong. They arrive in the register of a right answer, which is exactly why they are expensive. A hesitant wrong answer you double-check. A confident wrong answer you paste into your code and meet again on Thursday.

I have a small collection now. The model that did arithmetic wrong in the middle of an otherwise correct explanation, stated as flatly as the correct steps around it. The one that cited a config option that has never existed. The one that described, in detail and with total assurance, how a tool works, while describing a different tool.

None of these mean the tools are useless. They mean fluency and correctness are separate axes, and half of using these things well is developing a nose for when a plausible answer has quietly crossed the edge of what the thing actually knows.

So let us trade them, partly because they are funny and partly because collecting the specific shapes is how you build that nose:

1. What is the dumbest thing your AI confidently got wrong this week? The more real it looked, the better.
2. Did anything tip you off, or did you only find out after acting on it? I want to know whether anyone has actual signal for "this one is confidently wrong," or whether we are all just checking everything now.

Drop your best one. I suspect the comments will be more useful than the post.
