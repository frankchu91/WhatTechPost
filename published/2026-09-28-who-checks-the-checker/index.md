<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/28 discussion 3/3. Grounded entirely in real findings from this week, no new claims:
  * 4 checks in my pipeline had never fired; 2 of them structurally could not
  * the duplicate-post bug was invisible to 6 per-file checkers for 24 days (34 as of 2026-10-04)
  * the aiscan threshold could be beaten by adding filler (score 9 -> 3, same 9 em dashes)
  * two readers found defects by executing code; no automated gate found either
- The question is the post. Ends on a real one.
-->

---
title: "Which check in your pipeline has never fired?"
published: false
description: "I audited my own and found four. Two of them had never fired because they were structurally incapable of firing, and I could not tell the two groups apart by reading the code."
tags: discuss, testing, devops, career
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-28-who-checks-the-checker/cover.png
---

I went through every automated check in my publishing pipeline this week and sorted them by how many times each had ever caught something. Four of them had never caught anything.

My first reaction was that this was good news. A check that never fires is a check whose class of problem you have stopped having, which is what you want. I held that opinion for about an hour.

Then I found a bug that had been live for twenty-four days and is still live a month later, sitting in front of all four of those checks, and realised that two of them had never fired for a completely different reason: they could not. Not "had no occasion to." Could not. The thing they were meant to catch was not visible from the data they were looking at, and no amount of occasion would have changed that.

The specific case, briefly, because the shape matters more than the details. All six of my checks took a file and examined it. The bug was that two of my posts existed twice on the platform under different URLs. That is not a property of any file. You can hand a per-file checker every file I own, run it forever, and it will never see a duplicate, because the duplicate lives in a relationship between my repo and a remote system that no single file knows about.

What unsettles me is that I could not tell the two groups apart by reading them. Both categories look identical in the code and identical in the logs. Both are a function that runs, examines something, and returns no findings. "Quiet because the problem is gone" and "quiet because I am blind to the problem" produce byte-identical output, and I had been reading that output as reassurance for weeks.

I have been trying to find a reliable way to distinguish them and I do not have one. A few things I have tried, none of which fully work:

Feed each check an input that should fail it. This catches the crudest version, where a check is misconfigured or its regex never matches. It caught one of my four. It does not catch the structural case, because to write the failing input you have to already understand what the check can see, and if you understood that you would have spotted the gap.

Look for checks that examine a narrower scope than the property they claim to verify. This is closer to the real test, and it is how I eventually found the blind one. A check named "is this post published correctly" that only ever opens one file is claiming something about a system while looking at a fragment. But phrasing it that way requires you to have written down what each check actually claims, separately from what it does, and I had not.

Delete a check and see if anything breaks. Appealing, and useless on any timescale I have patience for.

There is a related version of this that I think is more common and more expensive. One of my checks did fire, regularly, and was still not doing its job, because the threshold it compared against could be moved by padding the input. It passed things it should have failed while producing a steady stream of reassuring output. That is worse than the silent ones, because a check that fires sometimes looks alive.

And the two real defects that readers found in my published code this quarter were both found by someone executing the code, not by any tool. Every one of my gates checks form. Both defects were about whether a claim was true. I do not think that gap closes with more gates.

So the question I keep landing on is not "do you have enough checks." It is whether you can distinguish, for any given check, between these three states: it protects you and the problem stopped happening, it fires reliably but its threshold does not mean what you think, and it has never fired and never will.

Three specific things I would like to hear from people who maintain a CI pipeline older than a year:

1. Do you track which checks have ever failed in production, and have you ever deleted one for being silent too long? I suspect most teams accumulate checks and never retire any, which means the signal from "everything passed" degrades continuously and nobody notices the moment it stops meaning anything.

2. Has one of your checks ever turned out to be structurally incapable of catching what it was named for? I am curious whether there is a common shape to these. Mine was a per-item check on a property that only exists across items, and I wonder if that is the usual one.

3. For the things automation cannot check at all, what do you actually do? Code review is the standard answer and I do not find it satisfying, because the two bugs readers found in my work had both survived my own careful review. The thing that caught them was a different person with a different mental model running the code, which is a resource I do not know how to schedule.
