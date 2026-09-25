#!/usr/bin/env python3
"""audit.py — run every check this repo learned the hard way, over the whole archive.

Each check here exists because something it would have caught got published.
Usage:  python3 scripts/audit.py [path ...]   (default: published/ and drafts/)
Exit 1 if any ERROR-level finding is reported. WARN findings never fail the run.
"""
import ast, builtins, glob, json, os, re, sys, urllib.parse, urllib.request

FENCE = re.compile(r"^```([a-zA-Z0-9+_-]*)[^\n]*\n(.*?)^```", re.S | re.M)
LEAD_COMMENT = re.compile(r"\A\s*<!--.*?-->\s*", re.S)
FM = re.compile(r"(?ms)\A---\n(.*?)\n---\n")
BUILTINS = set(dir(builtins))
UA = {"User-Agent": "WhatTechPost-audit/1.0"}


def slice_post(raw):
    """The five checks below disagreed for months about what 'the post' is.
    One function now decides, and returns each region separately."""
    notes = (LEAD_COMMENT.match(raw) or [""])[0] if LEAD_COMMENT.match(raw) else ""
    rest = raw[len(notes):]
    m = FM.match(rest)
    front = m.group(1) if m else ""
    body = rest[m.end():] if m else rest
    return {"notes": notes, "front": front, "body": body}


def free_names(code):
    """Names a snippet reads but never binds. Over-approximates what's bound,
    so everything it reports is a real miss."""
    class S(ast.NodeVisitor):
        def __init__(s): s.bound, s.used = set(), []
        def _a(s, a): s.bound.add((a.asname or a.name).split(".")[0])
        def visit_Name(s, n):
            s.bound.add(n.id) if isinstance(n.ctx, ast.Store) else s.used.append(n.id)
        def visit_FunctionDef(s, n):
            s.bound.add(n.name); A = n.args
            for a in A.args + A.kwonlyargs + A.posonlyargs + [x for x in (A.vararg, A.kwarg) if x]:
                s.bound.add(a.arg)
            s.generic_visit(n)
        visit_AsyncFunctionDef = visit_FunctionDef
        def visit_ClassDef(s, n): s.bound.add(n.name); s.generic_visit(n)
        def visit_ExceptHandler(s, n):
            if n.name: s.bound.add(n.name)
            s.generic_visit(n)
        def visit_comprehension(s, n):
            for t in ast.walk(n.target):
                if isinstance(t, ast.Name): s.bound.add(t.id)
            s.generic_visit(n)
        def visit_Import(s, n): [s._a(a) for a in n.names]
        visit_ImportFrom = visit_Import
    s = S(); s.visit(ast.parse(code))
    return sorted({u for u in s.used if u not in s.bound and u not in BUILTINS})


# ---------------------------------------------------------------- checks

#: A block whose first line is a comment naming a source file is an excerpt —
#: a quotation of code that lives somewhere else, not a snippet to paste. Adding
#: an import line to make it satisfy this check would falsify the quote, so
#: excerpts are reported at WARN. The marker has to be written by hand, which
#: keeps the exception visible instead of silent.
EXCERPT = re.compile(r"\A\s*#\s*\S+\.(py|js|ts|sh)\b")


def check_missing_imports(path, R):
    """Cost: 16% of published python blocks raise NameError on paste."""
    for lang, code in FENCE.findall(R["body"]):
        if lang.lower() not in ("python", "py"):
            continue
        level = "WARN" if EXCERPT.match(code) else "ERROR"
        try:
            missing = [n for n in free_names(code) if n in sys.stdlib_module_names]
        except SyntaxError as e:
            yield level, f"python block does not parse: {e.msg}"
            continue
        if missing:
            yield level, f"python block uses {missing} with no import" + (
                " (excerpt)" if level == "WARN" else "")


def check_untagged_fences(path, R):
    """No language tag means no highlighting and no static check ever sees it."""
    n = sum(1 for lang, _ in FENCE.findall(R["body"]) if not lang)
    if n:
        yield "WARN", f"{n} fenced block(s) with no language tag"


def check_notes_not_leaked(path, R):
    """Deliberately does nothing at the file level.

    The first version of this flagged every archived file that still had its
    REVIEW NOTES comment, which was 91 false positives, because the archive is
    supposed to keep them. publish.py strips notes from the *payload*, not from
    the file. What matters is whether they reached the live post, and only the
    API can answer that — see leak detection inside reconcile()."""
    return iter(())


def check_no_published_flag(path, R):
    """A local mirror of remote state. It was wrong in 87 of 91 files."""
    if re.search(r"(?m)^published:\s*true", R["front"]):
        yield "WARN", "front matter claims published: true; the API is the only authority"


def check_cover_ratio(path, R):
    """Covers go through fit=cover at 1000x420. Wrong ratio means a silent crop."""
    m = re.search(r"(?m)^cover_image:\s*(\S+)", R["front"])
    if not m:
        yield "ERROR" if path.startswith("published/") else "WARN", "no cover_image in front matter"
        return
    local = os.path.join(os.path.dirname(path), os.path.basename(m.group(1)))
    if not os.path.exists(local):
        return
    with open(local, "rb") as f:
        head = f.read(32)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return
    w = int.from_bytes(head[16:20], "big"); h = int.from_bytes(head[20:24], "big")
    if (w, h) != (1000, 420):
        yield "ERROR", f"cover is {w}x{h}, not 1000x420; fit=cover will crop it"


def check_em_dash_density(path, R):
    """Density check, scoped to the body only. Front matter is not prose."""
    words = len(R["body"].split())
    n = R["body"].count("—")
    if words and n / words * 1000 > 12:
        yield "WARN", f"{n} em dashes in {words} words ({n/words*1000:.1f} per 1000)"


CHECKS = [check_missing_imports, check_untagged_fences, check_notes_not_leaked,
          check_no_published_flag, check_cover_ratio, check_em_dash_density]


def reconcile(paths):
    """The archive-wide check: does published/ agree with the API?"""
    key = os.environ.get("DEVTO_API_KEY") or _key_from_env_file()
    if not key:
        return ["WARN  reconcile skipped: no DEVTO_API_KEY"]
    arts, page = [], 1
    while True:
        req = urllib.request.Request(
            f"https://dev.to/api/articles/me/published?per_page=100&page={page}",
            headers={**UA, "api-key": key,
                     "Accept": "application/vnd.forem.api-v1+json"})
        batch = json.load(urllib.request.urlopen(req, timeout=30))
        if not batch:
            break                      # empty page, not short page
        arts += batch
        page += 1
    live = {a["title"] for a in arts}
    out = []

    # Count articles, not titles. Publishing has no idempotency key, so a
    # re-run of a partially failed batch silently creates a second copy.
    seen = {}
    for a in arts:
        seen.setdefault(a["title"], []).append(a)
    for title, copies in seen.items():
        if len(copies) > 1:
            ids = ", ".join(str(c["id"]) for c in copies)
            out.append(f"ERROR live duplicate x{len(copies)} (ids {ids}): {title[:50]}")

    # Notes leak into the live body or they don't. The file is not the evidence.
    #
    # The first version of this searched the whole body for "REVIEW NOTES" and
    # flagged exactly two posts: the one about checkers that confuse a mention
    # with a use, and the one that quotes the line which strips these comments.
    # Both were false positives, in a function written to prevent that bug.
    # A leak is a notes comment in the position publish.py strips from: the top.
    for a in arts:
        if LEAD_COMMENT.match(a.get("body_markdown") or ""):
            out.append(f"ERROR review notes leaked into live post {a['id']}: {a['title'][:50]}")

    for p in paths:
        if not p.startswith("published/"):
            continue
        raw = open(p, encoding="utf-8").read()
        m = re.search(r'(?m)^title:\s*"?(.*?)"?\s*$', slice_post(raw)["front"])
        if m and m.group(1) not in live:
            out.append(f"ERROR {p}: in published/ but not live on dev.to")
    out.append(f"info  {len(live)} posts live on the API")
    return out


def _key_from_env_file():
    try:
        for line in open(".env"):
            if line.startswith("DEVTO_API_KEY="):
                return line.split("=", 1)[1].strip()
    except OSError:
        return None


def main():
    args = sys.argv[1:] or sorted(
        glob.glob("published/*.md") + glob.glob("published/*/index.md")
        + glob.glob("drafts/*/index.md"))
    errors = warns = 0
    for p in args:
        raw = open(p, encoding="utf-8").read()
        R = slice_post(raw)
        found = [(lvl, msg) for c in CHECKS for lvl, msg in c(p, R)]
        if found:
            print(f"\n{p}")
            for lvl, msg in found:
                print(f"  {lvl:<5} {msg}")
                errors += lvl == "ERROR"; warns += lvl == "WARN"
    print("\n--- reconcile")
    for line in reconcile(args):
        print(" ", line)
        errors += line.startswith("ERROR")
    print(f"\n{len(args)} files · {errors} errors · {warns} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
