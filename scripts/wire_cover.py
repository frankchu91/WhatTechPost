#!/usr/bin/env python3
"""Insert cover_image into a draft's FRONT MATTER, scoped correctly.

Usage: python3 scripts/wire_cover.py drafts/<slug>/index.md

Why this exists: the inline one-liner this replaces tested `"cover_image:" not in text`
against the WHOLE file. On 2026-09-18 a post whose body discusses the `cover_image`
field matched that test, so the wiring step silently skipped it and the post published
with no cover at all (cover_image came back NULL from the API).

That is the same mention-vs-use scope bug that has now bitten every checker in this
repo. The fix is the same one: look only at the region you actually mean.
"""
import re
import sys

BASE = "https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published"
FM = re.compile(r"(?ms)^---\n(.*?)\n---\n")


def wire(path: str, base: str = BASE) -> str:
    raw = open(path, encoding="utf-8").read()
    slug = path.split("/")[-2]

    # Strip any leading REVIEW NOTES comment so its `---` lines can't be mistaken
    # for front-matter delimiters.
    lead = re.match(r"\A\s*<!--.*?-->\s*", raw, re.DOTALL)
    head, body = (lead.group(0), raw[lead.end():]) if lead else ("", raw)

    m = FM.match(body)
    if not m:
        return f"SKIP {slug}: no front matter block found"

    fm = m.group(1)
    if re.search(r"(?m)^cover_image:", fm):        # scoped: front matter only
        return f"ok   {slug}: already wired"

    new_fm = fm + f"\ncover_image: {base}/{slug}/cover.png"
    out = head + body[:m.start(1)] + new_fm + body[m.end(1):]
    open(path, "w", encoding="utf-8").write(out)
    return f"WIRED {slug}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        print(wire(p))
