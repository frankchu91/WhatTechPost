<!--
REVIEW NOTES (delete before publishing)
- FORMAT: practical/hands-on, AI-building lane (variety from the 3 pipeline posts). Broad evergreen audience (everyone parsing LLM output).
- Facts/code verified against current Claude API structured-outputs docs (claude-api skill, python/claude-api/tool-use.md): output_config.format with json_schema guarantees valid JSON; messages.parse(output_format=Model) -> parsed_output; strict:true tool with additionalProperties:false + required; structured output + citations = 400. OpenAI has response_format equivalent.
- Keep this comment free of the swap-table tell-words. No personal-take slot. NON-META. No AI-disclosure line. COVER: cover.png (HANDS-ON).
- DO NOT PUBLISH until the user says so (publish gate).
-->

---
title: "Stop asking the model for JSON. Constrain it."
published: false
description: "'Respond only in JSON' works in every test and fails in production with a fence, a preamble, or a trailing comma. The fix is to constrain the output to a schema, not to ask nicely."
tags: ai, llm, python, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-09-stop-asking-llm-for-json/cover.png
---

Every app that parses an LLM's output starts the same way. You end the prompt with "Respond only with valid JSON," it works in every test you write, and then it ships. A while later a request comes back wrapped in a ```json fence, or with a cheerful "Sure, here is the JSON:" in front of it, or with one trailing comma that makes `json.loads` throw at 2am. The failure is rare enough to pass review and common enough to page you.

I shipped that exact bug. Here is what actually fixes it, and why the thing everyone tries first cannot.

## Why "respond only in JSON" does not hold

A prompt is a request, not a constraint. The model is predicting plausible text, and "Here is the JSON:" is extremely plausible text to put in front of some JSON. You are asking a text predictor to please not predict text. Most of the time it obliges. Under load, on an unusual input, it does not, and no amount of rewording the instruction changes that, because prompting is not where guarantees come from.

The guarantee has to come from the decoder, not the prompt.

## Fix 1: constrain the output to a schema

Current APIs will hold the model to a JSON schema as it generates, so it cannot emit anything that does not match. On the Claude API you pass the schema in `output_config.format`:

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "Extract: John Smith (john@co.com), Enterprise plan."}],
    output_config={"format": {"type": "json_schema", "schema": {
        "type": "object",
        "properties": {
            "name":  {"type": "string"},
            "email": {"type": "string"},
            "plan":  {"type": "string"},
        },
        "required": ["name", "email", "plan"],
        "additionalProperties": False,
    }}},
)

import json
text = next(b.text for b in response.content if b.type == "text")
data = json.loads(text)   # guaranteed to parse and match the schema
```

No fence, no preamble, no trailing comma, because the decoder was never allowed to produce them. OpenAI has the same thing under `response_format` with a JSON schema. This is the real fix, and it is the one people skip because the prompt version looked like it worked.

If you are in Python, you can skip the manual parse entirely and hand the API a Pydantic model:

```python
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    email: str
    plan: str

response = client.messages.parse(
    model="claude-opus-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "Extract: John Smith (john@co.com), Enterprise plan."}],
    output_format=Contact,
)
contact = response.parsed_output   # a validated Contact instance, not a string
```

## Fix 2: if you are already in a tool loop, use a strict tool

When the JSON is really a function call, define the shape as the tool's `input_schema` and set `strict: true`. The arguments then arrive schema-valid:

```python
tools=[{
    "name": "book_flight",
    "description": "Book a flight",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "destination": {"type": "string"},
            "passengers":  {"type": "integer"},
        },
        "required": ["destination", "passengers"],
        "additionalProperties": False,
    },
}]
```

Same idea as a schema on the response, aimed at the tool arguments instead.

## Fix 3: validate anyway, because shape is not sense

This is the floor, not the ceiling. Even with constrained output, check the parsed object against your own rules and retry on failure. A schema guarantees the shape of the answer, never the truth of it. The model can hand you a perfectly valid string that is a hallucinated email, or an integer in the wrong unit. Constrained decoding makes the output parseable; your validation is still what makes it trustworthy.

## Three habits that still bite

Parse, never string-match. Do not fish values out of the raw output with a regex or a substring search. The exact JSON escaping varies between models and even between requests, so `json.loads` / `JSON.parse` is the only safe reader. Matching on the serialized text is a bug waiting for a backslash.

Valid is not correct. Schema-constrained output is shaped right and can still be wrong. Keep the semantic checks you would have written anyway; the schema does not replace them.

Watch the feature conflicts. Constrained output does not combine with everything. On the Claude API, for one, asking for a schema and citations in the same request is rejected. Check the combination before you wire it up, rather than after it returns a 400 in staging.

The whole shift fits in a sentence: stop asking for the format and start constraining it. "Respond only in JSON" is a hope, a schema the decoder enforces is a guarantee, and the gap between the two is exactly the set of 2am pages you will not get.

If you have hit a structured-output failure that slipped past a schema, I want to hear it, because those are the ones worth collecting.
