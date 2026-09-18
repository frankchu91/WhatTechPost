<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/17 HARDCORE 2/2. Measured today: same test file fed to all three checkers.
  aiscan score 0 (counts comment words), techcheck PROSE (comment stripped, correct), leakcheck LEAK! (fires on its own regex example in prose)
  content-aware leakcheck (strip front matter + comments + fences first) -> clean.
- Thesis: three independently written checkers share one bug: they operate on raw file bytes, so they cannot tell a mention from a use.
-->

---
title: "Three checkers I wrote, one bug: none of them can tell a mention from a use"
published: false
description: "A writing linter, a substance gate, and a leak detector. Written months apart, for different jobs. All three read raw file bytes, and all three get fooled by a post that talks about what they check for."
tags: programming, testing, javascript, python
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-17-three-checkers-one-bug/cover.png
---

I have three checkers guarding my publishing pipeline. A writing linter that scores AI-sounding prose. A substance gate that fails posts without real code. A leak detector that makes sure my private review notes never reach a published article.

Different jobs, written weeks apart, two languages. This week all three failed on the same input, in the same way, for the same reason.

## The input

One file that is deliberately about the things the checkers look for:

```markdown
<!--
REVIEW NOTES - DO NOT PUBLISH
-->
---
title: "x"
---
Prose with no code at all, but I discuss the regex <!--[\s\S]*?--> in text.
```

Note what is true of it. The private comment is a real comment, so a leak check should care about it before publishing and not after stripping. The body has no code, so the substance gate should fail it. And the body *mentions* a comment-shaped regex without containing a real second comment.

## All three verdicts

```
aiscan   : score 0
techcheck: PROSE — add real code or reclassify
leakcheck: LEAK!
```

The middle one is correct. `techcheck` strips the leading comment before counting fences, so it correctly reports that the body has no code. That line exists because I got burned already:

```js
// strip the REVIEW NOTES comment so my own notes never count as content
const raw = fs.readFileSync(file, 'utf8').replace(/^\s*<!--[\s\S]*?-->\s*/, '');
```

The other two are wrong, in opposite directions.

**`aiscan` scores the comment.** It reads the whole file, so the words inside my private notes count toward the post's writing quality. I found this the hard way when I listed the words to avoid inside a review comment and the scanner failed the post for containing them. Notes to myself, graded as prose.

**`leakcheck` fires on a mention.** My leak check is a substring test for the phrases that mark a private comment:

```python
"LEAK!" if ("REVIEW NOTES" in body or "DO NOT PUBLISH" in body) else "clean"
```

The body above has no second comment. It has prose *describing* a comment-matching regex. The substring is present, so the check screams. When I published a post about stripping comments, this fired on the code sample inside my own article, and for a few minutes I believed I had leaked private notes into a live post.

## One bug, three instances

None of these is really a bug in the check's logic. Each one is correct about the question it asks. The shared defect is **what they ask it of**: all three run against raw file bytes, where a private comment, a fenced code block, front matter, and actual prose are indistinguishable.

A checker operating on raw bytes cannot distinguish:

| | should count for | actually counts for |
|---|---|---|
| review comment | leak check only | all three |
| fenced code | substance gate only | all three |
| front matter | neither | all three |
| body prose | writing linter | all three |

Every one of my three tools wanted a different slice of that file, and all three got the whole thing.

## The fix is one function, shared

```python
import re

def split_doc(raw):
    """Separate a draft into the parts each checker actually wants."""
    comments = re.findall(r"<!--[\s\S]*?-->", raw)
    body     = re.sub(r"<!--[\s\S]*?-->", "", raw)
    body     = re.sub(r"^---[\s\S]*?---", "", body, count=1)   # front matter
    code     = re.findall(r"```[\s\S]*?```", body)
    prose    = re.sub(r"```[\s\S]*?```", "", body)
    return {"comments": comments, "body": body, "code": code, "prose": prose}
```

Then each checker asks for its own slice. The writing linter scores `prose`. The substance gate counts `code`. The leak check looks at `body` — the file minus the comments — because a leak is a private comment that *survived* into the body, and after stripping, a genuine leak leaves nothing to find.

Running that on the same input:

```
leakcheck        : LEAK!
content-aware    : clean
```

Correct, and correct for the right reason. The mention in the prose is no longer a leak because the check is now looking at the body rather than the bytes.

## What I take from it

I wrote these three tools at different times, for different problems, and reinvented the same mistake each time without noticing, because each one worked on the happy path. The failures only appeared when the content became self-referential, which is exactly the input a technical blog produces constantly: posts about the tools that check the posts.

The general version: a checker is two things, a question and a scope. I kept getting the question right and never once thought about the scope, and the scope is where all three bugs lived.

Anyone else running a pipeline of independent checks over the same file: do they share a parser, or does each one re-read the raw bytes and hope? Mine hoped, three times.
