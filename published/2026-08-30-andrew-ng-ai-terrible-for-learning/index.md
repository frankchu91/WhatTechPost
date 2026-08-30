<!--
REVIEW NOTES (delete before publishing)
- COVER: cover.png · QUOTE CARD: quote.png (Ng "terrible for learning")
- Source: Andrew Ng interview transcript (provided by author). Commentary/analysis with the author's own builder take — NOT a recap. Quotes are from the transcript; attribute to Ng.
- HARD RULE: no Meta. The transcript's "Metamuse is a good model" line is deliberately not used. Do not add any Meta/Llama/Muse reference.
- Ties to the author's own published post: 90% adoption / junior-dev ladder — cross-link it.
- Written to pass aiscan. Re-run node scripts/aiscan.js before publishing.
- No AI-disclosure line (policy).
-->

---
title: "Andrew Ng says AI is 'terrible for learning.' For developers, that's the warning worth hearing"
published: false
description: "The person who taught AI to millions thinks it's great for getting work done and quietly bad at making you better. For builders, that gap is where the real career risk lives."
tags: ai, career, productivity, learning
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-30-andrew-ng-ai-terrible-for-learning/cover.png
---

In a new interview, Andrew Ng, who helped build this field and taught AI to millions of people, said something most AI enthusiasts will not say out loud: "frankly AI models are terrible for learning." Not that the tools are dangerous. Not that the jobs are gone. Something quieter, and for developers more useful. He loves AI for getting work done and uses it constantly. He also thinks it is bad at the one thing that keeps you valuable over time.

That is worth taking seriously, because Ng is about the last person you would expect to talk AI down, and because I feel the exact effect he is describing in my own work.

![Andrew Ng: "Frankly, AI models are terrible for learning. It's absolutely terrible for learning."](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-08-30-andrew-ng-ai-terrible-for-learning/quote.png)

## The offloading trap

Ng's point rests on a distinction we blur constantly. Getting work done and learning are not the same activity, and AI is excellent at the first and poor at the second. He cites the data: college students who use AI score higher on their homework and retain less, because the AI did the work for them. Then he gives his own version, which every developer will recognize. He used a model to work out how some front-end and back-end pieces fit together, got the answer, shipped it. Six months later he needed to do it again, did not remember, and asked the AI a second time.

That is cognitive offloading, and Ng is careful to say it is not a bad thing on its own. It is how society gets work done. The problem starts when you mistake it for learning. You did not learn the thing. You rented the answer. Renting is fine right up until the moment the thing you rented is the thing your value depended on.

## Why this is bigger than homework

Here is where it connects to another point Ng makes, and where it stops being about your GPA and starts being about your career. He argues the durable human advantage over AI is context, which he calls the technical basis for judgment and taste. You know the customer's face fell when you demoed the feature. You know why the team walked away from that pattern two years ago. You know which line in the generated code is lying, because you once wrote that bug yourself. AI does not have any of that, and Ng thinks it will not for a long time, which is exactly why humans stay necessary.

Now notice how context gets built. It gets built by doing the work, the same work AI now does for you. The judgment that makes you valuable is the residue of a thousand small tasks you struggled through. Offload all of them and you stay productive this quarter while you quietly stop accumulating the thing that makes you hard to replace. That is the trap in one sentence. AI can make you more productive and less knowledgeable at the same time, and the bill for the second half arrives late.

## The junior-developer version is worse

I wrote recently that ninety percent of developers now use AI agents weekly, and that the bottom rung of the career ladder, the small well-defined tasks, is exactly what agents do best.

{% link https://dev.to/frankchu/90-of-developers-now-use-ai-coding-agents-weekly-the-interesting-question-isnt-whether-its-1je1 %}

Ng's learning point sharpens that into a real problem. Those beginner tasks were never only output. They were how people built the judgment to review harder work later. If a generation skips them because the AI is faster, where do the next people who can tell good generated code from plausible-looking generated code come from?

Ng is not fatalistic about it, and neither am I. His answer is that the skill map shifts, and the people who thrive go learn the new skills instead of giving up because someone told them AI made learning pointless. Universities are slow, he says, still teaching the jobs of 2022, so the move is to pick up the 2028 skills wherever you can find them. In his telling, the fear-mongering mostly just makes people quit early, which is the one guaranteed way to lose.

## What I actually do about it

The fix is not "use less AI." It is being deliberate about which half you are doing. Ng frames the job math this way: AI can do maybe thirty to forty percent of the tasks, and that makes the other sixty to seventy percent, the judgment and the taste and the deciding what to build, more valuable rather than less. Use AI to erase the part that is now cheap. Guard the part that is not.

For me that means one rule: I let AI write the code, but I do not let it write code I do not understand. If I cannot review it, explain it, or reconstruct why it works, I have not shipped a feature. I have planted something I will have to ask the AI about again in six months. On the tasks that build context, the debugging, the design calls, the reasons behind a choice, I do enough by hand to keep the muscle. On the mechanical work, I offload freely and feel no guilt.

That is the whole balance Ng is pointing at. AI is a fantastic way to get work done and a poor way to learn, so do your getting-done with it and protect your learning from it. The developers who come out ahead will not be the ones who used AI the most, or the least. They will be the ones who stayed the valuable sixty percent while letting the machine have the other forty.

If you have found a way to ship with AI without letting it hollow out what you know, I would like to hear the rule you use, because "productive but not learning" is the quiet failure mode nobody warns you about.
