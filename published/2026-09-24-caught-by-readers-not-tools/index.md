<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/24 discussion 3/3. Real: two published defects found by readers executing the code (@pm25coder stubbed-clock retry budget; @obole population mismatch). My own three automated gates caught neither, by construction.
-->

---
title: "My linters have never found a real bug in my posts. Readers have found two."
published: false
description: "I run three automated checks before anything publishes. In two weeks, readers found two defects in code I'd already shipped. The gates caught neither, and it isn't because the gates are bad."
tags: discuss, testing, programming, career
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-24-caught-by-readers-not-tools/cover.png
---

I have three automated checks standing between a draft and the publish button. One scores the writing for machine-sounding patterns. One fails anything that claims to be technical without real code in it. One makes sure my private review notes never leak into a live post.

In two weeks they have caught: some filler words, a few em-dashes, and a post that was prose pretending to be a tutorial. Useful, all of it.

In the same two weeks, readers found two actual defects in code I had published. One person took a retry helper out of a post, ran it against a stubbed clock, and showed that my 45-second budget would run for 120 seconds when the server sent a `Retry-After` header, because I checked the budget before sleeping instead of comparing it to the sleep. Another re-ran a query from a different post and found I had compared a 68-item dataset against a 60-item one, because a page size had truncated silently.

Both were real. Both were in the part of the post a reader would copy. My three gates had nothing to say about either, and I want to be precise about why, because "add more linting" is the wrong lesson.

The checks I built all answer questions about **form**. Does this text have the shape of machine writing. Does this file contain fenced code. Does this body contain a private comment. Those are decidable by looking at the artifact, which is exactly why I could automate them.

What the readers checked was **whether the thing is true**. Does this function respect its own stated budget. Do these two numbers describe the same set of things. You cannot answer either by inspecting the text. You have to execute it, or reproduce the query, and then compare the result against what the prose claims. That is not a linting problem with a harder linter at the end of it; it is a different category of question.

The uncomfortable part is that I reviewed both posts carefully and approved both defects. I am not a reliable checker of my own claims at the moment I finish making them, and the tooling I built to compensate was built to catch the mistakes I already knew I made. It could never have caught the ones I did not know about, because I designed it from my own model of my failures.

There is a version of this that ends in "so write tests for the code in your blog posts," and I do not think that is quite it either. The retry helper was illustrative, twelve lines, the kind of snippet nobody tests. The point is not the test. The point is that someone with a different mental model ran it and found out, and that is a resource I cannot build in a script.

So I am starting to think of the comment section as the only part of my verification pipeline that can check semantics, which reframes what a correction is. It is not embarrassment to be minimised. It is the most expensive kind of review I get, and I do not pay for it.

Two things I want to know:

1. Has an automated check in your own setup ever caught something that would have shipped as a bug, or do yours also mostly catch style? I am curious whether my split is typical or whether I built the wrong gates.
2. When someone corrected something you shipped publicly, did you fix it visibly or quietly? I have started leaving the correction in the post with the person's name on it, and I am not fully sure that is right, only that a silent edit reaches none of the people who already copied the broken version.
