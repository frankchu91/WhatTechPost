<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 10/07 HARDCORE 1/2. Prompted by a real comment from @danorie on the linter post (2026-10-01).
  They run a checker with the same mixed scoring: em dashes per 1000 words, banned-phrase set where
  a strong tell costs on first hit and soft ones get two free passes, all summed into an A-D grade.
  Their question, verbatim in substance: "Did you try a minimum-words floor on the density terms
  instead, so a 78-word body can't be judged as if it were an essay?"
- Measured today. Floor on the denominator, same 9 em dashes:
    words  raw/1k  floor100  floor250  floor500
       48   187.5     90.0     36.0     18.0
       78   115.4     90.0     36.0     18.0
      123    73.2     73.2     36.0     18.0
      198    45.5     45.5     36.0     18.0
      348    25.9     25.9     25.9     18.0
      648    13.9     13.9     13.9     13.9
     1248     7.2      7.2      7.2      7.2
  At 648 words a floor of 500 is already inactive -> the floor cannot stop the padding attack.
- Archive body word counts (code stripped), 106 posts: min 337, p10 488, median 670, max 1199.
  Posts under 100 words: 0. Under 250: 0. Under 500: 12 (11%). So floors of 100/250 are no-ops here.
- Built the split instead. Attack re-run, same 9 dashes + 2 phrase tells, growing filler:
    x0   REVIEW (2 phrase tells: robust, seamless; 9 em dashes 163.6/1k)
    x40  REVIEW (2 phrase tells: robust, seamless; 9 em dashes 13.7/1k)
    x80  REVIEW (2 phrase tells: robust, seamless)          <- density clears, phrase holds
    x160 REVIEW (2 phrase tells: robust, seamless)
- New gate over 106 published posts: 66 PASS (62%), 40 REVIEW (37%). Families firing:
  phrase 35, metadata 23, em-dash 21. Old gate passed nearly everything.
- Important: the density test now parses the ratio out of the issue text instead of reusing
  r.score, because r.score is the AGGREGATE. Using it as "the density score" would rebuild the
  exact bug under a name that hides it.
-->

---
title: "A reader asked if a word-count floor would fix my linter. I measured it, and it fixes a different bug."
published: false
description: "Someone running the same kind of checker suggested clamping the denominator so a short body isn't judged like an essay. It is a good fix. It does nothing about the hole I actually had."
tags: javascript, testing, tooling, writing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-10-07-floor-or-split/cover.png
---

I published a post last week showing that my writing checker could be beaten by padding: the same nine em dashes scored 9 at 78 words and 3 at 648, because the density terms and the phrase terms were being summed into one number. A reader named @danorie replied with something better than agreement.

They run a checker with the same structure. Em dashes scored per thousand words, a banned-phrase list where a strong tell costs points on its first hit and the soft ones get two free passes, everything summed into a single A-to-D grade. Same mix, same consequence: a padded draft can buy its way from B to A. They had not noticed until reading the post, which is the part I would have missed from the inside.

Then they asked a question I had not considered: did I try a **minimum-words floor on the density terms**, so that a 78-word body cannot be judged as if it were an essay?

I had not. So I measured it.

## What the floor actually does

The idea is to clamp the denominator upward. Instead of dividing by the real word count, divide by `max(words, floor)`. Same nine em dashes in every row:

```
words  raw/1k  floor100  floor250  floor500
   48   187.5     90.0     36.0     18.0
   78   115.4     90.0     36.0     18.0
  123    73.2     73.2     36.0     18.0
  198    45.5     45.5     36.0     18.0
  348    25.9     25.9     25.9     18.0
  648    13.9     13.9     13.9     13.9
 1248     7.2      7.2      7.2      7.2
```

Read the left side first, because that is where the floor earns its keep. A 48-word fragment with nine em dashes reports 187 per thousand, which is a number about a document that does not exist. Nobody wrote a 48-word post; they wrote a fragment, and extrapolating its punctuation rate to essay scale is meaningless. The floor fixes that, and it is a real bug.

Now read the right side, which is my problem. My attack moves a body **up** the table. At 648 words a floor of 500 has already stopped applying. Every floor at or below the padding target is inactive by definition, because the whole point of the floor is to stop binding once the document is long enough to measure honestly.

So the floor and the padding attack operate on opposite ends of the same axis and never meet. The floor cannot close a hole that lives above it.

## And on my corpus it does nothing at all

I checked whether a floor would change anything in practice, which required knowing how short my shortest post actually is:

```
body word counts across 106 published posts (code stripped):
  min 337   p10 488   median 670   max 1199

  posts under 100 words:   0   (0%)
  posts under 250 words:   0   (0%)
  posts under 500 words:  12  (11%)
```

Nothing under 250 words. A floor of 100 or 250 is a no-op on everything I have ever published. A floor of 500 would touch twelve posts, all of them short discussion pieces where the shorter length is the format rather than an accident, so clamping their denominator would make their scores *less* informative, not more.

That is worth separating from the first result. The floor is a correct fix for a failure mode I do not have. If my corpus included 80-word notes or changelog entries, I would want it. It would have been easy to implement it anyway, feel like I had addressed the comment, and ship a change that provably could not fire on my own inputs. I have published a post about exactly that mistake, and I nearly made it again inside the week.

## The split, built this time

@danorie's first suggestion was the one that matters, and it is the one I had described in print without building: split the verdict rather than the score. Any strong tell is a hard fail regardless of length; only the density checks get to be ratios.

```js
const PHRASE = new Set(['tier1', 'tier1-clarity', 'tier2', 'hollow-intensifier',
                        'transition', 'lets-construction', 'real-actual-inflation']);
const phraseIssues = r.issues.filter((i) => PHRASE.has(i.type));

const emIssue = r.issues.find((i) => i.type === 'em-dash');
const emCount = emIssue ? parseInt(String(emIssue.text), 10) : 0;
const emPer1k = r.stats.wordCount ? (emCount / r.stats.wordCount) * 1000 : 0;

const fails = [];
if (phraseIssues.length) fails.push(`${phraseIssues.length} phrase tell(s)`);
if (emCount > 9 || emPer1k > 12) fails.push(`${emCount} em dashes (${emPer1k.toFixed(1)}/1k)`);
if (metaIssues.length) fails.push(`${metaIssues.length} metadata tell(s)`);

const verdict = fails.length ? `REVIEW / REWRITE (${fails.join('; ')})` : 'PASS';
```

One detail in there took me a second attempt. My first version wrote `if (r.score > TARGET)` for the density family, because the aggregate score was already sitting there. But `r.score` **is** the aggregate, phrase contributions included. Using it as "the density score" would have rebuilt the precise bug I was fixing, under a label that hid it. The density test now parses the ratio out of the issue's own text, so it measures only what it claims to.

The attack, re-run against the split. Nine em dashes and two phrase tells throughout, filler growing:

```
filler x0    REVIEW (2 phrase tell(s): robust, seamless; 9 em dashes (163.6/1k))
filler x40   REVIEW (2 phrase tell(s): robust, seamless; 9 em dashes (13.7/1k))
filler x80   REVIEW (2 phrase tell(s): robust, seamless)
filler x160  REVIEW (2 phrase tell(s): robust, seamless)
```

At x80 the density term clears, correctly: nine em dashes in twelve hundred words really is fine. The phrase tells do not clear, because they never could. The hole is closed, and it is closed by removing the averaging rather than by tuning a number.

## What it cost

The new gate is meaningfully stricter than the old one:

```
over 106 published posts:   PASS 66 (62%)   REVIEW 40 (37%)
families firing:  phrase 35   metadata 23   em-dash 21
```

The old single-threshold gate passed nearly all of those. I am not going back and rewriting thirty-seven posts, but everything from here has to clear a bar that most of my archive would not have.

Two things I took from this that were not in my own post. One: a suggestion can be entirely correct and still not apply, and the only way to know is to run it against your actual inputs rather than against the argument. Two: the person who told me which of my two options to build was someone looking at their own tool with the same defect, which is a kind of review I cannot generate by thinking harder about mine.

If you maintain a scoring gate of any kind, what families are you summing that should not be summed? I would guess most people with a single numeric threshold have at least one pair.
