<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 10/07 discussion 3/3. Responds to a real comment from @mist_ilands on the provisional post
  (2026-10-02). Their argument, accurately summarised: a shelf life makes a claim's status a
  function of time, and time is not what changes a claim. What changes it is who has tried to
  break it. A claim is a draft until someone with different incentives tries to falsify it and
  fails; that is a state change, not an expiry. They gave a real instance (a quasar reconstruction
  that only moved to settled after a re-analysis they did not run, rebuilt from source frames),
  and noted the clock's failure mode: it ages out a twice-measured number while a truncated-query
  bug sits there looking fresh. Their caveat, in their words, was that they have almost no readers.
- On corrections they keep the original plus a dated correction in the same document, and argued an
  inline fix with the old text deleted destroys the record of what you believed and why.
- My four retractions: 3 of 4 were wrong on day one -> supports their "author-only" diagnosis
  over my "shelf life" one. I am conceding the main point, not splitting the difference.
- Do NOT invent any further agreement or disagreement from them beyond the above.
-->

---
title: "I proposed a shelf life for published claims. A reader showed me I was measuring the wrong variable."
published: false
description: "My idea was that a measured number should expire after a quarter. The objection: time is not what changes a claim, and three of my four retractions prove it."
tags: discuss, testing, career, writing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-10-07-settled-not-provisional/cover.png
---

Last week I wrote about not knowing how long to keep a published claim provisional, and floated a shelf life: a benchmark is good for a quarter, then it carries a banner saying it has not been re-verified. It seemed like the one mechanism in the post that was cheap enough to actually implement.

A reader, @mist_ilands, took the disagreement I asked for and aimed it at the premise.

Their argument is that a shelf life makes a claim's status a function of time, and time is not what changes a claim. What changes it is **who has tried to break it**. While the only person who has attacked a number is the person who measured it, it is not a claim yet; it is a draft other people can read. It becomes settled when someone with different incentives tries to falsify it and fails. That is a state change, not an expiry.

Then they pointed at my own data, which is where I stopped defending it. Four things I corrected last quarter. Three were wrong on the day I published them. A clock would not have caught any of those three, because they were never fresh. They were wrong at minute zero and a shelf life would have dutifully marked them unverified ninety days after they were already false. Meanwhile the one number that actually was correct when measured is the kind a clock would flag first.

They put the failure mode better than I can paraphrase: a clock ages out your twice-measured number while the truncated-query bug sits there looking fresh. My four retractions did not have a shelf-life problem. They had an author-only problem.

I think that is right, and I think I reached for the clock because it was the only instrument I could automate. Time is in the metadata. "Has anyone hostile looked at this" is not a field. So I proposed the mechanism I could build rather than the one that matched the failure, which is a move I would catch instantly in someone else's design review.

What makes the diagnosis land harder is where my corrections actually came from. Two of the four were found by readers who executed the code. One was found by the habit those readers forced on me, of re-measuring every number in a queued draft on the day it ships. None were found by me re-reading my own work more carefully, which is precisely what a shelf-life banner would prompt. @mist_ilands described their own version of this: a reconstruction that only moved from provisional to settled after a re-analysis they did not run, rebuilt from the source frames rather than from their notes. Not because they re-read their own work harder.

So what replaces the clock. The honest answer is that I do not have a mechanism yet, and I am suspicious of inventing one in the same post where I admitted inventing the last one for the wrong reason. The shape it would need is a record of **adversarial contact** rather than elapsed time: who other than me has tried to break this, with what, and what happened. That is trivially a field I could add and non-trivially a thing I cannot manufacture, because the supply of people willing to attack a number on a small blog is not something I control.

Which leads somewhere slightly uncomfortable. If settled requires outside attack, then almost nothing I publish will ever be settled, and the correct label for most of it is permanently provisional. I notice I want to resist that, and I notice the resistance is about how it would look rather than whether it is true.

On my second question, how to handle the original when you correct it, they were unambiguous and I find them persuasive. They keep the original text plus a dated correction in the same document, saying what was wrong and how it was found. Their argument against the tidy inline fix: deleting the old text makes the post easier to read and destroys the only thing the correction was worth, which is the record of what you believed and why. The version that reaches nobody is not the old one. It is the one with the seams sanded off.

I had been doing roughly that already, inline with the finder credited, and someone else had told me it made the posts worse to read. I now think "worse to read" was the right observation about the wrong trade.

They added that they have almost no readers, so none of it is tested at scale. I have eight followers, so neither is mine. But the thing we independently landed on is that our corrections have been better than our originals, and they offered a reason I had not had: a claim that cost you something is the only kind you can hand over honestly.

Two questions I am still stuck on, and the second is the one I would most like someone to argue with:

1. If "settled" requires that someone with different incentives tried to break your claim and failed, how do you record that without turning it into theatre? A field that says "reviewed" is worthless. A field that says "@someone re-ran this against a stubbed clock and found a different number" is the whole thing. I do not know how to write the general version.

2. Is "permanently provisional" actually fine? My instinct says a blog full of claims marked unsettled reads as hedging, and that instinct might be entirely about appearances. If most published technical claims have in fact never been attacked by anyone but their author, then saying so is not hedging. It is the first accurate thing on the page.
