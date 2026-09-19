<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/19 non-technical 3/3. Style: discussion. Real: a commenter reproduced my retry function with a stubbed clock and showed cap_seconds=45 + Retry-After 120 returns after 120s. I verified it and got the same numbers.
-->

---
title: "The best comment I ever got was someone proving my code wrong"
published: false
description: "Someone ran my published function with a stubbed clock and posted the numbers. My wall-clock budget was 45 seconds and it ran for 120. I'd rather have that comment than a hundred reactions."
tags: discuss, programming, career, testing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-19-best-comment-i-got/cover.png
---

I published a post with a retry helper in it. A budget guard, exponential backoff, the usual shape. It looked fine to me and it looked fine to the several people who read it.

Then someone left a comment that had actually run it.

They stubbed the clock, zeroed the jitter so the runs were deterministic, and reported two cases. With a 45-second budget and a server sending `Retry-After: 120`, my function returned after 120 seconds, having made two attempts. With a 2-second budget and no header, it returned after 3.

I reproduced it and got identical numbers. They were right. My budget check sat before the sleep, so a single long `Retry-After` blew straight through the limit and the function only noticed on the next iteration, after the time was already spent. A wall-clock cap that can only detect an overrun after the overrun is not a cap.

They found two more things in the same comment. That `e.retry_after or wait` silently discards the backoff whenever the server does send a header, and that the header can be an HTTP-date rather than a number of seconds. And that my outer attempt count multiplies with the SDK's own default retries, so a logical call I thought had four attempts could be a dozen HTTP requests.

Three real defects, with a reproduction, in a comment on a blog post.

My first reaction was not gratitude, I will be honest. It was the small flush you get when someone shows your work is wrong in public. That lasted about a minute, and then it was replaced by something better, which is that I now have correct code and I did not have to find the bug myself.

Here is what makes that comment rare, and it is not the tone. It is that they ran it. Most feedback on technical writing, including most of the good feedback, engages with the argument. This engaged with the artifact. They took the function out of the post, put it on a test bench, and came back with numbers. That converts a disagreement into a fact, and there is nothing to argue with afterward.

I have been thinking about it as the difference between a reader and a reviewer. A reader tells you what they thought. A reviewer tells you what happened when they tried it. The second one is enormously more work and it is the only kind that can find a bug you have already looked at and approved.

It also changed what I think a comments section is for. I had been treating engagement as a proxy for reach, which is a slightly grubby way to think about it. Under that framing a correction is a cost. Under the framing I actually want, a correction is the highest-value thing the section can produce, and a hundred agreeable reactions are worth less than one person who opened a REPL.

## What I did with it

I reproduced their result, fixed all three defects, and pushed the corrected code back
to the live post. Then I did the part I had to think about for a minute: I left the
correction visible instead of quietly swapping the code.

```
Correction (2026-09-17). The version that first shipped here checked the budget
before the sleep but never compared it to how long the sleep would be, so a single
Retry-After: 120 blew straight through a 45-second cap...
```

The instinct was to edit silently. The post would look like it had always been right,
and almost nobody would ever know. I talked myself out of it on a practical argument
rather than a noble one: anyone who already copied that function needs to find out,
and a silent fix reaches exactly zero of them. The credit line costs me nothing and
is the only thing that makes the correction discoverable.

So:

1. What is the best correction you have received on something you published or shipped? I mean the one you were glad about afterward, not the one that was just right.
2. Have you ever done this for someone else, actually run their code before commenting? I have not, often enough, and after this week I think that is the thing I should copy rather than the writing advice.
