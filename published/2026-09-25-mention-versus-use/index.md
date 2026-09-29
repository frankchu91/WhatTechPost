<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/25 discussion 3/3. Five real instances from this repo, all the same class:
  1. aiscan counts tell-words inside my REVIEW NOTES comment (notes about the writing, scored as the writing)
  2. techcheck counted code fences inside that same comment until I stripped it
  3. leakcheck fired on a regex quoted in prose that matched its own leak pattern
  4. wire_cover.py skipped a post because the string "cover_image:" appeared in the body text
  5. aiscan scores front matter: identical body, title changed, score 0 -> 42 (measured today)
- Instance 5 measured today with byte-identical bodies confirmed by comparison.
-->

---
title: "Every checker I wrote this month had the same bug: it could not tell using a word from talking about one"
published: false
description: "Five tools, five different jobs, one shared defect. Each of them read a region of the file that looked like content but wasn't, and every fix was the same shape."
tags: discuss, programming, testing, tooling
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-25-mention-versus-use/cover.png
---

I changed the title of a draft last week. Nothing else. The body was byte-identical, which I checked rather than assumed. My writing checker went from a score of 0 to a score of 42 and flipped from pass to rewrite.

The title was deliberately terrible, so the flag was fair. What was not fair is that the title is not the article. It renders as the headline and the social card; it is not prose a reader wades through. My checker had no idea there was a difference, because it read the file as one undifferentiated blob of text.

Then I went back through the other tools I have written for this repo, and found I had shipped the same mistake five times.

A word-level checker counted flagged words inside the HTML comment at the top of my drafts, the one where I write notes to myself about the writing. Notes about tell-words, scored as tell-words. A gate that requires a post to contain real code counted the fenced blocks inside that same comment, so a post could pass by having code in its review notes and none in its body. A check that makes sure private notes never leak into a published file fired on a post that discussed the leak pattern in prose, because the prose contained the pattern. A script that wires a cover image into front matter skipped a post whose body happened to contain the words `cover_image:` in a code sample.

Five tools, five unrelated jobs. Same defect. Each one was handed a file and treated every byte of it as the thing it was checking, when in fact the file has regions with different meanings: notes that are not content, metadata that is not prose, quoted examples that are not claims.

Philosophers have a name for this, the use-mention distinction, and it is the difference between *cat* has three letters and a cat has four legs. It sounds like a word game until you write a tool, and then it turns out to be the entire problem. A linter that cannot distinguish a word you are using from a word you are discussing will flag every article about bad writing, including this one.

What makes it hard to notice is that the failure is always plausible in isolation. The tool ran. It produced a number. The number was even defensible if you squinted, since the title really does contain the word it flagged. Nothing crashes. You only catch it by constructing the case where the two readings diverge, and you only think to construct that case if you already suspect the bug exists.

Every fix turned out to be the same move: decide explicitly which slice of the file the tool is about, extract that slice, check only it. Three lines each time. The thinking was the expensive part, and it was the same thinking five times without me recognising it on the second, third, or fourth occasion.

I am not sure what the generalisation is. Part of me says the tools should share a parser, so that "the body of a post" is defined once instead of re-derived by each script from its own regex. That is clearly right for this repo. But I do not think it explains the pattern, because the scripts were written weeks apart for different reasons, and at no point while writing any of them did the question "what counts as the content here" feel like an open question. It felt like the file was obviously the content. That is the part I would want to fix, and it lives upstream of the code.

A postscript I did not expect to be writing. Since drafting this I collapsed those five scripts into one, specifically to fix this class of bug in one place, and the consolidated tool committed the same error twice more on its first two runs. Seven instances now. Knowing the failure mode, while actively writing about the failure mode, protected me from nothing.

Two things I would like to know from people who build this kind of tooling:

1. Does your linter, formatter, or scanner know which parts of a file are the subject and which are scaffolding? I am specifically curious about documentation and content tooling, where front matter and quoted examples are the norm rather than the exception. My suspicion is that this is near-universal and mostly invisible because nobody writes the adversarial case.

2. When you find the same bug class in the fifth place, what do you actually do about it? Writing one shared helper is the obvious answer, and I will probably do it, but the honest problem was that I did not recognise instances two through four as the same thing at the time. Is there a way to get better at that, or is noticing it on the fifth try just what the process looks like?
