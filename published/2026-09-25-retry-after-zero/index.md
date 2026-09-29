<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/25 HARDCORE 2/2. Real header from dev.to today: 403, server Varnish, retry-after: '0', body 0 bytes.
- Hot-loop demo measured against a local stub that replays that exact response.
  Re-measured 2026-09-29, 10 repetitions, 12-core M2 Pro, load average 7.61:
    naive   (trusts Retry-After) 5 requests in 1.3-15.0ms = 332-3896 req/s, median 3634
    guarded (floor 1s, cap 30s)  5 requests in 5.025s     = 1.0 req/s
  The 9/24 run of the SAME code gave 187 req/s under load average 70. Reporting the range
  and the conditions instead of one number, per the benchmark-retraction post already live.
- dev.to 403 headers re-verified 2026-09-29: server Varnish, retry-after '0', no x-request-id, body 0 bytes.
- Technique credit: @pm25coder, who found a bug in my earlier retry code by running it against a stubbed clock.
  This is the same move applied to a stubbed server.
-->

---
title: "A server sent me Retry-After: 0 and my retry loop lost its brakes"
published: false
description: "I trusted a header. The header said zero. The loop that was supposed to back off politely emptied its entire retry budget in milliseconds, at the thing that had just blocked me."
tags: python, api, reliability, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-25-retry-after-zero/cover.png
---

While tracking down an unrelated 403 last week I printed the full response headers, and one of them stopped me:

```
status      : 403
server      : Varnish
retry-after : '0'
body length : 0
```

`Retry-After: 0`. I had a helper in the same repo whose entire job is to read that header and sleep for that long, and I could see immediately what it would do with a zero. What I could not do was guess the magnitude, so I measured it.

## The loop, and what it actually does

This is close to what I had, and close to what turns up if you search for how to handle a 429:

```python
import time, urllib.request, urllib.error

def naive_retry(url, attempts=5):
    for i in range(attempts):
        try:
            return urllib.request.urlopen(url, timeout=5)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 503):
                wait = int(e.headers.get("Retry-After", 2 ** i))
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("out of attempts")
```

The `2 ** i` fallback is the part that makes it look safe. Exponential backoff is right there in the code, so the function reads as if it backs off. But the fallback only runs when the header is missing. When the header is present, whatever it says wins, and the carefully written backoff never executes at all.

I did not want to test this by hammering a real service, so I stood up a stub that replays the exact response I got: 403, `Retry-After: 0`, empty body. That technique is not mine. A reader named @pm25coder found a defect in an earlier version of this same helper by running it against a stubbed clock, which was the first time it occurred to me that you can test a retry policy without waiting for it.

```python
import http.server

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        HITS[self.path] += 1
        self.send_response(403)
        self.send_header("Retry-After", "0")
        self.send_header("Content-Length", "0")
        self.end_headers()
```

Five attempts against it, ten repetitions, on a 12-core M2 Pro at load average 7.6:

```
naive  (trusts Retry-After)   5 requests in 1.3ms - 15.0ms   (332 - 3896 req/s, median 3634)
guarded (floor 1s, cap 30s)   5 requests in 5.025s           (1.0 req/s)
```

The loop I would have described to you as "it backs off between attempts" completes its entire retry schedule inside a single frame of video, and every one of those requests goes to a machine that has just told me to go away.

I want to be careful about that range rather than quote you one number, because I ran the same code five days ago and got 187 req/s. Not a different result. A different afternoon: my laptop was under a load average of 70 at the time from an unrelated experiment. The spread within today's ten runs alone is twelve-fold.

So the throughput figure is a property of the machine, and the only part that transfers is the shape. Five attempts is nothing; what matters is that the count scales with whatever you set `attempts` to, scales again with however many workers run the same helper, and does all of it at the exact moment the far side is least able to absorb it. The right mental model is not "187 requests a second." It is "as fast as your process can issue them, with the brakes disconnected."

## Where a zero comes from

I do not think anyone typed `Retry-After: 0` as advice. Reading the RFC, the header takes either a delay in seconds or an HTTP date, and nothing forbids zero. My best guess is that this is a template with an unset variable rendering to its zero value, on a response path that was never meant to be retried at all, since the body is empty and the rejection is permanent for that client.

Which is the general case, not a quirk of one site. `Retry-After` is a number chosen by a machine that does not know anything about your workload, sent on a path that may not have been thought about carefully, and your client obeys it without question. The other failure mode is the same bug with the sign flipped: I have seen `Retry-After: 86400` on a transient error, which turns a five-second blip into a worker that sleeps for a day.

So treat it as input, not instruction:

```python
import time, urllib.request, urllib.error

def guarded_retry(url, attempts=5, floor=1.0, cap=30.0):
    for i in range(attempts):
        try:
            return urllib.request.urlopen(url, timeout=5)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 503):
                hdr = e.headers.get("Retry-After")
                try:
                    wait = float(hdr) if hdr is not None else 2 ** i
                except ValueError:          # it can also be an HTTP date
                    wait = 2 ** i
                wait = min(max(wait, floor), cap)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("out of attempts")
```

Three things changed, and each one fixes a separate failure.

`float()` instead of `int()`, inside a `try`. The spec allows an HTTP-date, and `int("Wed, 21 Oct 2026 07:28:00 GMT")` raises `ValueError` from inside your error handler, which is a fun way to lose the original exception.

`max(wait, floor)` is the one that fixes today's bug. A server's idea of an acceptable request rate is not binding on your client's idea of a sane one.

`min(wait, cap)` fixes the opposite bug, the one that has probably cost me more hours in aggregate: a process that looks hung but is politely asleep.

## The wider version

The honest lesson is not about this header. It is that my code had a defensive-looking default sitting next to an unconditional trust of remote input, and the default is what I saw when I read the function back. `2 ** i` is visible. `int(header)` is also visible. What is invisible is that the second one makes the first one dead code in exactly the situation you wrote it for.

I went looking for the same pattern elsewhere in the repo afterwards and found two more: a page size from a response used directly as a loop bound, and a timeout read from a config file with no upper limit. Both had a reasonable-looking fallback that a remote value silently outranked.

The grep that finds these is not clever. Look for anywhere a number crosses the boundary into your process and reaches `sleep`, `range`, `timeout`, or a buffer size without passing through a `min` or a `max` on the way.

What is the worst value a remote server has ever handed your client that your client simply believed? I would like to collect a few of these, because I suspect the zero is not even the funny one.
