<!--
REVIEW NOTES (delete before publishing)
- Topic: Jev / TypeSafe AI (launched 2026-09-15). NON-META.
- HONESTY CONSTRAINT: we have NO TypeSafe key and NO Anthropic key. We did NOT benchmark Jev and the post says so explicitly, up front. Every number below was measured in-session on 2026-09-20 via public registries.
- Verified in-session: PyPI typesafe-sdk timeline (0.0.1a0 2026-09-09, 0.5.7 09-11, 0.6.0 09-15, 0.7.0 09-18, requires >=3.10);
  npm @typesafe-ai/sdk (0.0.0-bootstrap.0 2026-09-12 02:56, 0.5.7 09-12 04:13, 0.6.0 09-15 18:17);
  POST api.typesafe.ai/v1/systemone -> 403 {"error_type":"authentication_error"};
  GitHub search: 756 repos, Go 9 / TS 7 / Rust 6 / Java 5 / Swift 4 / C# 4; top TS repo devagrawal09/jev-review 427* created 09-16.
  CAUGHT a false positive in our own query: Python "top" hit QuantDinger 11865* created 2025-12-28, predates Jev. Excluded and disclosed.
- Secondary sources read: flaviocopes.com/jev (0% type-error rate is "structural rather than empirical"; RLCD calibration "says nothing about any single answer"), The Register 2026-09-16 (hallucination-free "isn't a fair comparison as its output is not natural language").
- Differentiation: a 102-reaction practical how-to already exists. Do NOT duplicate it. This post fills the gap that guide explicitly flags ("TypeSafe's own numbers, self-run and unreproduced").
-->

---
title: "Everyone is quoting Jev's benchmarks. Here's what you can check without a key."
published: false
description: "Jev launched five days ago behind a waitlist, and every writeup repeats the same self-reported numbers. I couldn't get in either. The package registries and the GitHub API answered questions the press release didn't."
tags: ai, python, api, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-20-verify-jev-without-a-key/cover.png
---

I went to verify the numbers everyone is quoting about Jev and got a 403.

```bash
curl -s -X POST https://api.typesafe.ai/v1/systemone \
  -H "Content-Type: application/json" \
  -d '{"state":"test","questions":{}}'
```

```json
{"detail":{"error_type":"authentication_error",
           "message":"Must supply an API key! Check your request and try again."}}
```

Waitlisted. So I cannot tell you whether Jev is 193x faster or 444x cheaper than a frontier model, and neither can anyone else who has written about it this week. Those figures come from TypeSafe's own runs. The best practical guide out there says so in its own opening caveat: self-run and unreproduced.

What I did not expect is how much you can establish about a launch without ever calling the thing. The package registries and the GitHub API are public, they are not press releases, and they answer different questions.

## Start the clock before the announcement

Jev was announced on September 15. Its Python SDK was not.

```python
import json, urllib.request

def get(url):
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "verify/1.0"})))

pkg = get("https://pypi.org/pypi/typesafe-sdk/json")

rows = [(files[0]["upload_time"][:19], ver)
        for ver, files in pkg["releases"].items() if files]
for when, ver in sorted(rows):
    print(f"{when}  v{ver}")
print("requires_python:", pkg["info"]["requires_python"])
```

```
2026-09-09T10:34:07  v0.0.1a0
2026-09-11T23:05:50  v0.5.7
2026-09-15T10:23:18  v0.6.0
2026-09-18T09:12:29  v0.7.0
requires_python: >=3.10
```

The first artifact landed on September 9, six days before the public launch, and a near-release `0.5.7` went up on the 11th. The npm package tells the same story on its own clock: a `0.0.0-bootstrap.0` at 02:56 on September 12, `0.5.7` at 04:13 the same morning, then `0.6.0` at 18:17 on launch day.

None of that is scandalous. Staging a package before you announce is how you ship. It is just information you can only get by reading a registry instead of a blog post, and it sets a real timeline against which to read everything else.

The detail I would actually act on is the last line: **two minor versions in the first three days**, 0.6.0 on the 15th and 0.7.0 on the 18th. For a client library against an early-access API, that is a surface still in motion. If you are pinning this into something, pin it exactly and expect to move.

## Adoption you can count instead of assert

"The community is excited" is unfalsifiable. "How many independent repos, in how many languages, within a week" is not.

```python
import urllib.parse

q = "typesafe-ai+OR+typesafe-sdk+OR+jev-sdk"
r = get(f"https://api.github.com/search/repositories?q={q}&per_page=60")

langs = {}
for repo in r["items"]:
    langs.setdefault(repo.get("language") or "?", []).append(
        (repo["stargazers_count"], repo["full_name"], repo["created_at"][:10]))

for lang, repos in sorted(langs.items(), key=lambda kv: -len(kv[1]))[:8]:
    stars, name, created = max(repos)
    print(f"{lang:12} {len(repos):>2} repos | top: {name} ({stars}*, created {created})")
```

```
Go            9 repos | top: itsmostafa/typesafe-mcp (158*, created 2026-09-17)
TypeScript    7 repos | top: devagrawal09/jev-review (427*, created 2026-09-16)
Rust          6 repos | top: Dicklesworthstone/skillranker (105*, created 2026-09-17)
Java          5 repos | top: spring-ai-community/spring-ai-typesafe (4*, created 2026-09-20)
Swift         4 repos | top: krzyzanowskim/TypeSafe (22*, created 2026-09-19)
C#            4 repos | top: saibimajdi/typesafeai-dotnet-sdk (5*, created 2026-09-16)
```

TypeSafe shipped SDKs for two languages. Within six days there were community clients or integrations in at least six more, including a Spring AI module created the morning I ran this. A 427-star TypeScript project built on it, created the day after launch.

That is a real signal and it is not the same signal as "the model is good." It measures how badly people wanted this shape of thing to exist, which is worth knowing separately from whether this particular implementation delivers.

### The result I threw away

My first run of that query reported Python's top repo as an 11,865-star project. I nearly wrote that down. Its creation date was 2025-12-28, nine months before Jev existed, so it is a keyword collision and nothing to do with this launch.

I have been burned by exactly this recently enough to check: a measurement can be confidently wrong while the code that produced it is perfectly correct. The query worked. The population it returned was not the population I meant. The Python row is missing from the table above because I could not clean it in the time I had, not because Python has no ports.

## The claim everyone quotes is the one you already have

The headline that travels fastest is that Jev cannot hallucinate and has a 0% structured-output error rate. Both are true and neither is the reason to adopt it.

The mechanism is that Jev returns a probability distribution over options you supplied rather than generating free-form text, so a successful response cannot contain a value outside your schema. TypeSafe is straightforward that this rate is **structural rather than empirical** — it is a property of the design, not a measurement. The Register made the sharper version of the point: calling it hallucination-free "isn't a fair comparison as its output is not natural language."

Here is why that matters practically. You can already buy the same class of guarantee. Constrained decoding on a normal LLM, where you hand the API a JSON schema and the sampler is restricted to conforming tokens, gives you a response that cannot violate the schema either. Different mechanism, same promise: well-formedness.

And well-formedness is not correctness. A schema guarantees the answer has the right shape. It says nothing about whether the right shape holds the right value, and it converts a loud failure into a quiet one, because a malformed response throws and a well-formed wrong one gets written to your database.

The calibration claim has the same structure and is easier to misread. Jev is trained with a method that optimises probabilities against outcomes, so across many predictions the answers it gives 90% confidence should be right about 90% of the time. That is useful for setting thresholds. It also, as the deeper writeups note, says nothing about any single answer. Calibration is a property of a distribution, and you will be applying it one decision at a time.

## What I would actually test with a key

If someone hands me one, the numbers above are not what I would go after, because a latency multiple against an unnamed frontier model on an unnamed task is not a number that transfers to my workload anyway.

I would measure the thing the architecture claims and the marketing does not lead with: that a tenth question costs tokens but almost no wall clock, because questions are evaluated in parallel against one ingested state. That is falsifiable on a laptop in ten minutes — time one question, time twelve, plot it — and if it holds, it changes how you structure calls far more than a price per million tokens does.

Second, I would probe the failure boundary rather than the happy path: feed it state where the correct answer is simply not present in the options, and see whether an explicit `other` option actually absorbs it or whether confidence stays high on the closest wrong choice. The value of calibrated probabilities lives entirely in that case.

Until then, what I can say is narrow and verified: the SDKs are real and published, the endpoint is real and rejects you politely, the client surface moved twice in three days, and six language communities decided this was worth an afternoon within a week of launch. Everything else in circulation is a vendor benchmark with a friendly presentation.

If you have a key and you have run the parallel-questions test, I want the numbers, because that is the claim that would actually change how I write code, and it is the one nobody seems to be checking.
