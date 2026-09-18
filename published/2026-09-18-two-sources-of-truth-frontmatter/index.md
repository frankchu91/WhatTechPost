<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/18 HARDCORE 2/2. Measured today against live article 4671289:
  body_markdown round-trips the FULL front matter text, AND title/tag_list exist as parsed fields.
  publish.py's prepare_body sends front matter inside body_markdown and flips published: false -> true by regex.
- The risk this creates: PUT sends a whole body; if the front matter in your local file drifts from what you intend, you rewrite the post's metadata as a side effect of a body edit.
-->

---
title: "dev.to stores your front matter twice, and a body edit can rewrite your title"
published: false
description: "The API keeps your YAML inside body_markdown and also parses it into real fields. I checked a live post to see which one wins, because PUT replaces the whole body and I wanted to know what else it replaces."
tags: python, api, webdev, programming
---

I script my publishing to dev.to, and edits go up as a `PUT` that replaces `body_markdown` wholesale. Before trusting that with anything important I wanted to know one thing: when I replace the body, what else am I replacing?

The answer turns out to be more than the body, because the same information exists in two places at once.

## What actually goes over the wire

My publisher does almost nothing to the file. It strips the review-notes comment, flips the draft flag, and sends the rest:

```python
text = re.sub(r"\A\s*<!--.*?-->\s*", "", text, count=1, flags=re.DOTALL)
if publish:
    text = re.sub(r"^published:\s*false\s*$", "published: true",
                  text, count=1, flags=re.MULTILINE)
```

So what reaches the API still has the YAML on top:

```
'---\ntitle: "T"\npublished: true\ndescription: "d"\ntags: ai, llm\ncover_image: https://x/c.png\n---\n\nBody line.\n'
```

Front matter survives into `body_markdown`. That is by design: dev.to accepts a whole markdown document, metadata included.

## Both copies exist on the server

Here is the part I had not thought through. I pulled a live post back down and looked at what the API returns:

```python
a = get("https://dev.to/api/articles/4671289")

a["body_markdown"][:120]
# '---\ntitle: "The dev.to API can edit a published post. The quickstart never says so."\npublished: true\ndescription: "I pub'

a["title"]     # 'The dev.to API can edit a published post. The quickstart never says so.'
a["tag_list"]  # ['python', 'api', 'webdev', 'programming']
```

The YAML text is stored verbatim inside `body_markdown`, **and** the same values exist as parsed top-level fields. The platform reads your front matter, extracts title and tags into real columns, and keeps the raw text too.

Two representations of one fact, which is the setup for every synchronization bug ever written.

## Why that matters for an edit

`PUT` with a new `body_markdown` is a full replacement. If the new body contains front matter, the platform re-parses it, and the parsed fields follow whatever the YAML now says.

Which means **a body edit is also a metadata edit**, whether you intended one or not. Change the `title:` line in your local file to fix a typo in the markdown and you have renamed the live post. Drop a tag from the YAML while editing a paragraph and the post loses that tag. Remove the front matter entirely from your local copy and send just the prose, and you have sent a document whose title and tags are absent.

None of that announces itself. The API returns 200 and a normal-looking article object.

I checked the one thing I most cared about, and it survived:

```
slug still: the-devto-api-can-edit-a-published-post-the-quickstart-never-says-so-71c
```

The slug is generated at creation and does not change when the title does, so existing links keep working even if you rename a post. That is a relief and also a new hazard: the URL can now disagree with the title, permanently, and nothing will tell you.

## The rule I settled on

Keep one source of truth and make the direction of flow explicit.

```
repo file (front matter + body)  ──PUT──>  dev.to
                                 (never the other way)
```

The local markdown file is authoritative for everything, metadata included. I never touch the web editor, because anything I change there will be silently discarded the next time I push a body. And because the front matter rides along with every edit, I treat a change to those five YAML lines as a real change, reviewed like code, not as configuration I can tweak while I am in there fixing a sentence.

The thing I would tell my earlier self: when an API accepts a document that contains its own metadata, you no longer have an endpoint that edits the body. You have an endpoint that replaces the record, and the body is just the part you were looking at.

If you publish through an API that parses metadata out of the payload, have you hit the case where an unrelated edit moved a field you did not mean to touch? I suspect it is common and mostly noticed late.
