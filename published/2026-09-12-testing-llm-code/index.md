<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- Day 3 (9/12), post 2/3. FORMAT: practical/hands-on AI-building. Broad, evergreen.
- VERIFIED current-API nuance: sampling knobs (temperature/top_p/top_k) are REMOVED on current Claude models (Opus 5/4.8/4.7, Sonnet 5, etc. — 400), so "set temperature=0 for determinism" is STALE advice. Correct move: don't depend on exact text; mock in unit tests, assert structure in integration tests. This is the distinctive, first-hand-correct detail.
- aiscan-clean; no banned words in comment. NON-META. No AI-disclosure line. COVER: cover.png.
-->

---
title: "How to test code that calls an LLM without writing flaky tests"
published: false
description: "The moment your code calls a model, tests get slow, costly, and non-deterministic. Most people respond by not testing that path. Here's how to test it properly instead."
tags: ai, llm, testing, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-12-testing-llm-code/cover.png
---

The moment your code calls a model, your tests get slow, expensive, and non-deterministic. The common response is to just not test that path, which is the worst of the options, because the LLM call is usually sitting in the middle of the logic most likely to break. You can test it well. You just cannot test it the way you test a pure function, and one piece of old advice for making it deterministic no longer works.

## Unit tests: mock the model

Most of the code around an LLM call is deterministic and deserves normal, fast unit tests. Prompt assembly, response parsing, the retry logic, the routing decision, the fallback path, none of that needs a live model to test, and all of it is where your real bugs live. Mock the client, return a canned response, and test that your code does the right thing with it. A unit test that hits the real API is slow, costs money on every run, and flakes when the provider hiccups, so it fails at being a unit test on three counts. Keep the model out of them.

## Do not assert on exact text

Model output varies between runs, so `assert result == "expected string"` is a flaky test by construction. Assert on the things that are stable instead. Did it return valid JSON matching your schema? Does the parsed object have the required fields? Does the summary mention the entity it was supposed to? If you need the output shape to be reliable enough to assert on at all, constrain it with structured output so the structure is guaranteed and only the wording varies. Test the contract, not the prose.

## The determinism trick that stopped working

The old move was to set `temperature=0` for near-deterministic output you could pin a test to. On the current generation of models that is not available: the newer Claude models, for instance, removed the sampling parameters entirely and reject `temperature` with an error, and they are not alone in moving away from the knob. So building a test around "temperature zero gives me the same string every time" is now both brittle and, on many models, not even possible.

The better habit was always the same: do not depend on exact text. Once your assertions are about structure and properties rather than the literal output, it stops mattering whether the model is deterministic, and your tests survive the next model upgrade instead of breaking on it.

## Integration tests: real calls, but not on every commit

You still want a few tests that hit the real model, because mocks cannot catch a prompt that quietly stopped working against the current model. Keep them separate from the unit suite and run them on a schedule, not on every push, so a provider blip does not redden a PR. Have them assert on structure plus a semantic check, a property the answer must have, or a second model grading the first, so they catch real drift without demanding an exact string.

## Record and replay

The bridge between the two is capturing real responses once and replaying them. Hit the model a single time, save the responses as fixtures, and have the tests replay those. You get the realism of real output with the speed and determinism of a mock, and you refresh the fixtures deliberately when you change the prompt or the model rather than paying for a live call on every test run.

The throughline is that LLM code is testable as long as you stop treating the model's exact words as the thing under test. Mock it in units, constrain and assert structure in integration, replay fixtures for speed, and never pin a test to a string the model is free to reword. The path everyone skips is very much testable. It just needs tests written for a non-deterministic dependency, which the model has been all along.

If you have a pattern for testing LLM code that has held up, I want to see it, because this is the part of the stack with the least settled practice and the most teams quietly winging it.
