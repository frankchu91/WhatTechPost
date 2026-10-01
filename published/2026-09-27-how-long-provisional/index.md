<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/27 discussion 3/3. Grounded in real retractions from my own archive, all measured this week:
  * published 2.3s/render as a "fixed cost"; re-measured 0.93s, load average 70.59 at original measurement
  * published a 68-post figure against a 60-post figure; per_page=60 truncation, reader @obole caught it
  * published a retry helper whose 45s budget ran 120s; reader @pm25coder caught it with a stubbed clock
  * claimed self-referential posts don't get read, from a single top post; grouped data said 7.4 vs 7.1 avg
  * 5th case added 2026-09-30: a draft quoted 187 req/s for a hot retry loop (measured under load avg 70).
    Re-measured before shipping: 332-3896 req/s, 12x spread in one session. Caught by the draft's own
    re-verification step, not by a reader — the only one of the five caught before publishing.
- No new claims here. The question is the post.
-->

---
title: "How long do you keep a published claim provisional?"
published: false
description: "Four things I published this quarter turned out to be wrong, and three of them were wrong on the day I published them. I'm trying to work out what the right shelf life for a claim is."
tags: discuss, career, writing, testing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-27-how-long-provisional/cover.png
---

I retracted a benchmark this week. Two weeks ago I published a timing figure, described it as a fixed cost, and built an argument on it. Today the same script on the same machine ran two and a half times faster, and the reason was that I had taken the original reading while my laptop was under a load average of 70 from an unrelated experiment.

That is the fourth thing I have had to correct this quarter. One was a number I measured under conditions I did not record. One compared two populations of different sizes because a page size truncated a query. One was a retry helper with a budget that did not hold, found by a reader who ran it against a stubbed clock. One was a conclusion about which of my posts get read, drawn from a single data point, which fell over as soon as I grouped the data properly.

Three of those four were wrong on the day I published them. Not superseded by events. Wrong at the moment of writing, with the evidence available to me at the time, and I did not know it.

There is a fifth that did not make it out, and it is the one that changed how I think about this. A draft of mine quoted a throughput figure for a misbehaving retry loop: 187 requests a second. Before shipping it I re-ran the measurement and got a range of 332 to 3896, a twelvefold spread inside a single session, because the original number had been taken while my laptop was under a load average of 70. Nothing about the draft looked wrong. The only reason it was caught is that I now re-measure every number in a queued draft on the day it actually ships, and that habit exists solely because of the four above.

So the question I have been circling is not how to be more careful. I was reasonably careful on all five. It is what status a claim should have after I publish it, and for how long.

Right now I have two states, and I think that is the actual problem. Before publishing, a claim is under review and I will attack it. After publishing it becomes something I have said, and my posture flips from attacking it to defending it, or at least to not thinking about it. That flip happens at the moment of least new information, which is a strange place to put a phase change.

What I notice is that the flip is not really about confidence. It is social. Once something is public, revisiting it costs something, and the cost is not the two minutes of re-running a script. It is the small, stupid friction of having said a thing and now saying a different thing, to people who may have already repeated the first version.

A few ways I have seen people handle this, none of which I have committed to:

Some treat every published number as permanently provisional and version the post, leaving a visible changelog. That is honest but it turns a post into a maintained artifact, and I have maybe eighty of those now, which is not a maintenance burden I can carry.

Some set an expiry: benchmarks are good for a quarter, then they carry a banner saying they have not been re-verified. Cheap to implement. I like this more than I expected to, though it does not help with the three that were wrong immediately.

Some only publish claims they have reproduced under two different conditions. This would have caught my benchmark, since a second run on a quiet machine was all it took. It would not have caught the truncated query, because I would have reproduced the same wrong number twice.

And some just wait for readers, which is what has actually been happening to me. Two of the four were found by people who ran the code. That is a real mechanism and it works, but it only covers claims interesting enough that someone bothers, and it puts the cost on them.

The uncomfortable thing I keep arriving at is that the corrections have been better content than the original posts. The benchmark post was fine. The retraction, with the load average in it and the explanation of why a tight cluster is not evidence of a constant, is a more useful thing to have written. If that is generally true, then the thing I have been treating as a cost is closer to the product, and my instinct to publish carefully and then move on is backwards.

But I do not fully believe that either, because it has an obvious failure mode where you get sloppy on purpose and harvest the corrections. The people I read whose corrections are worth reading are people who were careful first.

Two questions, and I want disagreement on the first one especially:

1. Does your team or your writing have an explicit shelf life for a measured claim, or does a number stay true until someone complains? I am asking about the mechanism, not the intention. Everyone intends to revisit.

2. When you correct something publicly, what do you do with the original? I have been editing the live post with the correction inline and the finder's name attached, on the theory that a silent edit reaches nobody who already copied the wrong version. Someone told me that is worse, because it makes the post harder to read for everyone who arrives later and does not care about the history. I do not know who is right.
