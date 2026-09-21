<!--
REVIEW NOTES (delete before publishing)
- A practical Jev guide, written from the SDK SOURCE (typesafe-sdk 0.7.0 wheel from PyPI, unpacked and read on 2026-09-20), not from other people's writeups.
- HONESTY: no TypeSafe key, so nothing here is a benchmark and no output is invented. Every signature, default and type below is quoted from the shipped package.
- Verified in-session from the wheel:
  exports AsyncTypeSafeClient + TypeSafeClient, 12 typed error classes, Choice/Noul/Score + *Model TypedDicts, Answer discriminated union on "type"
  Noul.criteria is OPTIONAL NoulCriteria (descriptions of the yes and no outcomes); Choice.criteria is Mapping[str, JSONContent|None]; Score.criteria is Sequence[JSONContent]
  ScoreAnswer carries legend: dict[int,str|dict|list] AND probabilities: dict[int,float] keyed by int level
  system_one(state, questions, *, model, retry, timeout, extra_headers, extra_body, response_model) -> SystemOneResponse; response_model overload returns ResponseT
  constants: TYPESAFE_API_KEY, TYPESAFE_BASE_URL, DEFAULT_BASE_URL https://api.typesafe.ai, DEFAULT_MODEL jev-latest, DEFAULT_TIMEOUT 10.0, SYSTEM_ONE_PATH /v1/systemone
  RetryPolicy defaults: max_retries=2, backoff_initial=0.5, backoff_max=5.0, backoff_jitter=0.25; docstring example shows http_statuses={429,500,502,503,504}
- NON-META. Do not duplicate the existing popular how-to: this one is grounded in the source and covers async, errors, retry, response_model, legend — things the other guides skip.
-->

---
title: "Reading the Jev SDK source instead of the launch post"
published: false
description: "Jev is waitlisted, so I can't benchmark it. I can read the client. Pulling typesafe-sdk 0.7.0 off PyPI gives you the exact signatures, defaults, error types and retry policy, including the parts the guides skip."
tags: python, api, ai, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-20-jev-from-the-sdk-source/cover.png
---

I do not have a Jev key. The waitlist is real and `POST /v1/systemone` returns a polite 403 without one. So this is not a benchmark and there are no invented outputs below.

What I could do is read the client, which is published and does not care whether I have access:

```bash
python3 -m pip download typesafe-sdk --no-deps
unzip -q typesafe_sdk-0.7.0-py3-none-any.whl
find . -name "*.py"
```

An SDK is a contract written down. Every signature, default, and type in this post is quoted from that package rather than from a launch post, and a few of the useful parts are not in any guide I have read.

## What the package actually exports

```python
from typesafe_sdk._core.client.sync.client import TypeSafeClient
from typesafe_sdk._core.client.aio.client import AsyncTypeSafeClient
from typesafe_sdk._core.question_types import Choice, Noul, Score, Question, Questions
from typesafe_sdk._core.response_types import Answer, ChoiceAnswer, NoulAnswer, ScoreAnswer
from typesafe_sdk._core.errors import (
    TypeSafeAuthenticationError, TypeSafeRateLimitError, TypeSafeBadRequestError,
    TypeSafeNotFoundError, TypeSafePermissionDeniedError, TypeSafeUnprocessableEntityError,
    TypeSafeInternalServerError, TypeSafeAPIConnectionError, TypeSafeAPITimeoutError,
    TypeSafeAPIResponseValidationError, TypeSafeAPIError, TypeSafeError,
)
```

Two things stand out immediately. There is a **full async client**, `AsyncTypeSafeClient`, exported alongside the sync one. And there are twelve typed error classes, which means you can catch a rate limit distinctly from a bad request without string-matching a message. Neither shows up in the quickstart material.

## The defaults, from `constants.py`

```python
API_KEY_ENV      = "TYPESAFE_API_KEY"
BASE_URL_ENV     = "TYPESAFE_BASE_URL"
DEFAULT_BASE_URL = "https://api.typesafe.ai"
DEFAULT_MODEL    = "jev-latest"
DEFAULT_TIMEOUT  = 10.0
SYSTEM_ONE_PATH  = "/v1/systemone"
```

`DEFAULT_MODEL` being `jev-latest` is worth pausing on. A floating tag means the model under you can change without a deploy on your side. The client surface itself moved from 0.6.0 to 0.7.0 in the three days after launch, so if you want reproducible behaviour, pin the model explicitly rather than inheriting the moving target.

`DEFAULT_TIMEOUT = 10.0` is also a choice with a consequence. For a service that claims sub-second responses, a ten-second client timeout is generous, which tells you the failure they expect to protect you from is a hung connection rather than slow inference.

## The one call

```python
def system_one(
    self,
    state: JSONContent,
    questions: Mapping[str, Question],
    *,
    model: str | None = None,
    retry: RetryPolicy | None = None,
    timeout: float | httpx2.Timeout | None = None,
    extra_headers: Mapping[str, str] | None = None,
    extra_body: Mapping[str, JSONValue | None] | None = None,
    response_model: type[ResponseT],
) -> ResponseT: ...
```

`state` plus a dict of named `questions`, everything else keyword-only. The `response_model` parameter is an overload: pass nothing and you get a `SystemOneResponse`, pass a type and you get that type back, which is the hook for validating the envelope into your own model instead of theirs.

## The three question types, as the source defines them

This is where reading the code pays, because the three primitives take **structurally different** `criteria`, and the difference is not obvious from examples.

```python
class Noul:    # yes/no
    instructions: JSONContent | None = None
    criteria: NoulCriteria | None = None          # OPTIONAL: descriptions of the yes and no outcomes

class Choice:  # one label from a set
    instructions: JSONContent | None = None
    criteria: Mapping[str, JSONContent | None]    # REQUIRED: label -> description

class Score:   # position on an ordered scale
    instructions: JSONContent | None = None
    criteria: Sequence[JSONContent]               # REQUIRED: ordered levels, index IS the level
```

Three separate shapes. `Choice` is keyed by the label you want back. `Score` is a sequence where position carries meaning, so reordering the list silently changes what every stored score means. `Noul` is the only one where `criteria` is optional, and it takes a `NoulCriteria` describing the yes and no outcomes rather than a free-form string, which is the documented way to disambiguate a borderline question.

Also note `instructions` is typed `JSONContent`, not `str`, on all three. You can hand a question a structured object, not just a sentence.

## The answer types, and the field nobody mentions

```python
Answer: TypeAlias = Annotated[NoulAnswer | ChoiceAnswer | ScoreAnswer,
                              Field(discriminator="type")]
```

A discriminated union on `type`, so `match answer.type` is the intended way to branch, and Pydantic will reject a payload whose shape does not match its discriminator.

The interesting one is `ScoreAnswer`:

```python
class ScoreAnswer(wire.ScoreAnswer):
    legend: dict[int, str | dict[str, Any] | list[Any]]
    """Rubric descriptions keyed by integer score."""
    probabilities: dict[int, float]
    """Probabilities keyed by integer score."""
```

`legend` comes back with the answer. The response carries the rubric that produced it, keyed by integer level. That means a stored score is self-describing: six months later you can read a logged answer and know what level 2 meant at the time, without going to find the code that asked. For anything you persist and audit, that is the field to keep, and I have not seen it mentioned anywhere.

Both dicts are keyed by `int` while JSON object keys are strings, so the models coerce. If you serialise a `ScoreAnswer` yourself, expect the keys to come back as strings.

## Retry is already built, with real defaults

```python
@dataclass
class RetryPolicy:
    max_retries: int = 2
    backoff_initial: float = 0.5   # doubled each attempt, up to backoff_max
    backoff_max: float = 5.0
    backoff_jitter: float = 0.25   # fraction of each delay randomly subtracted
```

The docstring shows a custom policy retrying on `{429, 500, 502, 503, 504}`. Backoff with jitter is in the box, which is more than many SDKs ship.

The thing to notice is `max_retries: int = 2`, meaning up to three attempts per logical call **by default**. If you wrap this in your own retry loop, the two multiply: four outer attempts over three inner ones is twelve requests for one decision. Pick one owner. Set `max_retries=0` and own the loop, or drop your loop and tune the policy.

```python
from typesafe_sdk._core.retry import RetryPolicy

client.system_one(
    state=doc,
    questions={"urgent": Noul(instructions="This needs attention today")},
    retry=RetryPolicy(max_retries=0),   # I own the loop
    model="jev-0.6",                    # pin, don't float
    timeout=2.0,                        # fail fast; the service claims sub-second
)
```

## What reading the source does not tell you

It tells you the shape of the contract and nothing about whether the model is any good. Latency, cost, and accuracy all need a key and a real workload, and TypeSafe's published multiples are self-run and so far unreproduced.

What it does give you is a version of the API that cannot be out of date relative to the package you actually installed, which is more than can be said for any guide, including this one the moment 0.8.0 ships. The command at the top takes ten seconds and the answers are exact.

If you have access and have persisted `ScoreAnswer.legend` in anger, I want to know whether the rubric travelling with the answer actually saved you later, because that is the design decision in this SDK I find most interesting and the one I cannot evaluate from the outside.
