<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/26 HARDCORE 2/2. Re-measured 2026-09-26 over all 94 posts in published/ (the 9/24 figures drifted).
  118 fenced blocks total. By language: python 48, untagged 41, bash 11, js 6, yaml 5, json 2,
  markdown 2, ts 1, html 1, css 1.
  All 48 python blocks pass ast.parse (0 syntax errors) — that was the null result that led to the real check.
  Free-name analysis: 11 of 48 self-contained (22%), 37 reference undefined names (77%).
  61 distinct undefined names. Categories:
    stdlib modules never imported (7): html json re subprocess tempfile time urllib
    ALL-CAPS config constants (5): API_KEY ARTICLE_ID CHROME HEADERS TEMPLATE
    post-local helpers/types (49)
  7 of 48 blocks (14%) are missing at least one stdlib import.
- 41 of 118 fences have no language tag, so they get no highlighting.
-->

---
title: "77% of the Python I published references names it never defines"
published: false
description: "I extracted every code block from three months of posts and compiled them. All of them parsed. Then I checked whether they'd actually run, and the number got worse."
tags: python, programming, writing, testing
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-26-paste-my-code-and-it-breaks/cover.png
---

I wanted a cheap number for a different post, so I pulled every fenced code block out of my archive and ran each Python one through `ast.parse`. My expectation was that a few would be broken snippets and I would have a tidy confession to write.

```
posts: 94   fenced blocks: 118
python blocks: 48  — compiling each with ast.parse
  parse OK : 48
  SyntaxErr: 0  (0%)
```

Nothing. Forty-eight for forty-eight. I sat with that for a minute and then realised I had measured the wrong thing, because syntactic validity is a bar that a snippet clears by being typed carefully, and nobody's actual complaint about a code sample is that it fails to tokenise.

The complaint is that you paste it and it does not run. So I wrote the check for that instead.

## Free names

The question "would this run if you pasted it into an empty file" has a decent static approximation: walk the AST, collect every name the code binds, collect every name it reads, and subtract. What is left over is names the block expects to already exist. Anything not in `builtins` is something the reader has to supply.

```python
import ast

class Scope(ast.NodeVisitor):
    def __init__(s): s.bound, s.used = set(), []
    def _alias(s, a): s.bound.add((a.asname or a.name).split(".")[0])
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
    def visit_Import(s, n): [s._alias(a) for a in n.names]
    visit_ImportFrom = visit_Import
```

It is deliberately crude. It flattens all scopes into one, so it will not catch a name used before assignment, and it over-approximates what is defined. That means every name it reports is a real miss, and the true number is at least this bad.

```
python blocks that parse            : 48
  self-contained (all names defined): 11  (22%)
  reference undefined names         : 37  (77%)
```

Better than three quarters of them. Eleven blocks out of forty-eight can be pasted into a file and run.

## Not all misses are equal

A raw count gives you nothing to act on, because plenty of blocks are illustrative by design and should not carry twelve lines of setup. So I split the 61 distinct undefined names into three buckets, and the buckets turned out to be different problems with different answers.

```
stdlib modules never imported (7) : html json re subprocess tempfile time urllib
ALL-CAPS config constants (5)     : API_KEY ARTICLE_ID CHROME HEADERS TEMPLATE
post-local helpers and types (49) : get, api, client, spec, Question, Result, RetryPolicy, ...
```

The middle bucket is fine, and arguably good. `API_KEY` undefined is a signal to the reader that they supply their own, and writing `API_KEY = "sk-..."` in a post is worse than omitting it.

The third bucket is mostly fine too. If a block calls a helper I defined three paragraphs earlier, that is normal prose-with-code and re-declaring it in every snippet would be noise. Some of those 49 are type names from a library the post is about, where the import line is pure ceremony.

The first bucket has no defence at all. Seven stdlib modules, appearing across 7 of 48 blocks, fourteen percent of everything I have published. These are pure friction: someone pastes the snippet, gets `NameError: name 'subprocess' is not defined`, and now has to reconstruct which import I left out. It is the single easiest thing in this entire exercise to fix and it is the one I got wrong most often, because an `import` line at the top of a snippet feels like clutter while you are writing and feels essential the moment you are reading.

## The other 41

While I had the data out:

```
by language: python 48, (none) 41, bash 11, js 6, yaml 5, json 2, markdown 2, ts 1, html 1, css 1
```

Forty-one blocks with no language tag. Those are mostly terminal output and console logs, where untagged is a reasonable choice. But I spot-checked and some are real code that just never got a tag, which means no highlighting and no chance of a static check like this one ever seeing them.

## What goes in the pipeline

I already have a gate that fails a post claiming to be technical without enough code in it. It was counting blocks. Counting blocks is how you get 118 fences and 77% of them unrunnable.

```python
import ast, sys

def block_report(md):
    for lang, code in FENCE.findall(md):
        if lang.lower() not in ("python", "py"):
            yield lang, None
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            yield lang, f"SyntaxError: {e.msg}"
            continue
        free = free_names(tree)
        missing = [n for n in free if n in sys.stdlib_module_names]
        yield lang, f"missing import: {missing}" if missing else None
```

I am only making the stdlib-import case a hard failure. The other two buckets get printed as a warning and I decide per block, because "this snippet needs context from the post" is a legitimate authoring choice and a gate that forbids it would make every post worse.

That split matters more than the check. My first instinct was to require every block to be standalone, and I am fairly sure that instinct produces posts full of ceremonial imports and redeclared helpers that bury the four lines the post is actually about. The goal is not that every block runs. The goal is that a block which looks like it should run, does.

If you write technical posts, what is your rule for imports in snippets? I have been treating them as clutter for three months and the data says I was optimising for the wrong reader.
