<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/26 practical/evergreen 3/3. Every example is from a probe run this week against dev.to's API, not invented.
  Server: Varnish vs Heroku on 403 vs 200. x-request-id present only on 200. Content-Length 0 on the edge 403.
  Retry-After: 0 measured. per_page truncation re-measured 2026-09-26: 5->5, 60->60, 100->95, true total 95,
  no count field. (Was 92 on 9/24; the archive grew, which is exactly why the number is dated.)
- Deliberately the practical/evergreen lane: searchable, useful to someone who has never read my other posts.
-->

---
title: "Five things I read in an HTTP response before I read the status code"
published: false
description: "A week of debugging one API taught me that the status code is usually the least informative part of the response. Here's the order I check things in now, and what each one told me."
tags: api, debugging, python, webdev
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-26-five-response-details/cover.png
---

I lost about forty minutes this week to a 403 that had nothing to do with permissions, on an API I have been using daily for three months. The response had told me the answer immediately. I just was not reading that part.

Since then I have been going through responses in a fixed order before I let myself form a theory, and it has caught three things it would previously have taken me a while to find. The order is roughly "who answered, what did they say, and do they want me to come back."

## 1. `Server`, because it tells you which machine is talking

Every example here comes from the same endpoint, minutes apart:

```
403 response          200 response
  server: Varnish       server: Heroku
```

Two values means two different machines answered. Varnish is a cache in front of the application; Heroku is where the application runs. A rejection from the first one never reached the second, which immediately rules out every theory that involves application logic, including credentials, permissions, quotas, and your code.

This is the check with the best ratio of effort to information and it is the one I had never bothered with. Not every deployment exposes it, and plenty of stacks return the same value from every layer, but when it differs between a working and a failing request you have located the problem before you have started looking.

## 2. Whether the body is empty

```
403 -> content-length: 0     body: b''
401 -> content-type: application/json
       body: b'{"error":"unauthorized","status":401}'
```

Both of these are authentication-adjacent failures and only one of them explains itself. That is not an accident of who wrote the error handler. Applications know why they refused you and have a serialiser handy, so they tend to say. Edges and proxies are matching a pattern and dropping the connection, so they have nothing to say and often no JSON serialiser in the path at all.

A zero-length 4xx body is therefore weak evidence that you are talking to infrastructure, not to the service. Combined with point 1 it is usually conclusive.

## 3. Whether a correlation ID came back

```
200 -> x-request-id: 57878af6-2c5f-2391-8efc-8984dd2b59ea
403 -> (absent)
```

The application assigns the request ID. If it is missing, the application did not see your request. If it is present, it did, and you now have the one string that makes a support conversation productive instead of a description of your afternoon.

I have started logging it on every response, not just failures, because by the time you want it you cannot reproduce the request that had it. The header name varies by stack: `x-request-id`, `x-correlation-id`, `x-amzn-requestid`, `cf-ray`, `x-ms-request-id`. Grab whichever one exists.

## 4. `Retry-After`, and then don't trust it

The response I got carried this:

```
retry-after: 0
```

Zero. My retry helper read that header and slept for that long, which means five attempts completed in 27 milliseconds, all of them aimed at the machine that had just blocked me. Measured, at 187 requests per second.

The header is remote input, and nothing stops it being zero, or a date, or a number so large your worker naps for a day. Clamp it at both ends and keep your own backoff as the fallback:

```python
hdr = e.headers.get("Retry-After")
try:
    wait = float(hdr) if hdr is not None else 2 ** attempt
except ValueError:          # the spec also allows an HTTP-date
    wait = 2 ** attempt
wait = min(max(wait, 1.0), 30.0)
```

The `float` inside a `try` is not paranoia. `Retry-After` is legally an HTTP-date, and `int("Wed, 21 Oct 2026 07:28:00 GMT")` raises from inside your exception handler.

## 5. The length of a list, compared to what you asked for

This one is not a header, and it is the one that cost me an actual published mistake.

```
per_page=5     ->   5 returned
per_page=60    ->  60 returned
per_page=100   ->  95 returned
per_page=1000  ->  95 returned
```

The true total is 95. Every request below that came back exactly full, and the response body carries no total, no count, no next-page link and no has-more flag. From inside a single call there is no way to tell a complete result from a first page.

So the rule I now apply everywhere: if a collection comes back with a length exactly equal to the page size you requested, treat it as truncated. Real populations do not land on round numbers. A cheap version, when you do not want to write the pagination loop yet:

```python
rows = get(f"{url}?per_page={n}")
assert len(rows) < n, f"got exactly {n} rows; this is a page, not a result set"
```

It converts a silent wrong answer into a loud one, which is the trade I want on anything feeding a number I am going to act on.

## The actual habit

None of these are clever and I suspect most people reading this already knew four of them. The change that mattered was doing them in a fixed order, before forming a hypothesis, because the failure mode was never ignorance. It was that "403" has a meaning I have internalised, so reading it started a search for a permissions bug, and the search felt productive enough that I did not go back and look at the rest of the response for half an hour.

A status code is a three-digit summary written by whoever gave up on your request. The headers say who that was.

Which response detail do you check that I have not listed? I am building this into a helper and I would rather steal a sixth than discover it the way I discovered these.
