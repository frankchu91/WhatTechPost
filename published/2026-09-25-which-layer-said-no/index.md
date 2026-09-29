<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/25 HARDCORE 1/2. All probes run today against https://dev.to/api/articles, Python 3.14.6.
  403 -> server: Varnish, content-length 0, retry-after 0.  200 -> server: Heroku, x-request-id present.
  UA gate fires BEFORE auth: default UA + valid key = 403; custom UA + garbage key = 401 with a JSON body.
  Blocklist is a case-sensitive substring match on lowercase "urllib":
    urllib 403 / Urllib 200 / uRllib 200 / urlliB 200 / URLLIB 200 / urllib3 403 / URLlib3 200
  Blocked: python-urllib, urllib3, Java/17.0.1, empty UA.  Allowed: requests, httpx, aiohttp, curl, wget,
  okhttp, node-fetch, Go-http-client, scrapy/2.11.
-->

---
title: "The Server header told me which layer rejected my request, and it wasn't the one I was debugging"
published: false
description: "A 403 with a valid API key sent me looking for a permissions bug. The response header said Varnish, not Heroku, which meant my request never reached the application at all."
tags: python, api, debugging, webdev
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-25-which-layer-said-no/cover.png
---

I had a valid API key, the right `Accept` header, and a 403. So I did what you do: regenerated the key, checked the account, re-read the auth docs. None of it was the problem, and I had ignored the one header that would have told me so in the first minute.

```
--- request with the default Python UA -> 403
    server: Varnish
    content-length: 0
    retry-after: 0

--- request with User-Agent: WhatTechPost/1.0 -> 200
    server: Heroku
    content-type: application/json; charset=utf-8
    x-request-id: 57878af6-2c5f-2391-8efc-8984dd2b59ea
```

Two different values in `Server` means two different machines answered me. The 403 came from Varnish, a cache sitting in front of the app. The 200 came from Heroku, where the application actually lives. Whatever rejected me was not the thing that knows about API keys, because my request never got far enough for anyone to look at one.

## Proving the ordering

If the gate really sits in front of auth, then the key should not matter on one side and should matter on the other. That is a two-by-two you can just run:

```python
import urllib.request, urllib.error

def probe(ua, key):
    h = {"Accept": "application/vnd.forem.api-v1+json"}
    if ua:  h["User-Agent"] = ua
    if key: h["api-key"] = key
    req = urllib.request.Request(
        "https://dev.to/api/articles/me/published?per_page=1", headers=h)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.status, r.headers.get("server"), r.read()[:40]
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("server"), e.read()[:40]
```

```
default UA  + valid key    -> 403 Varnish  b''
default UA  + no key       -> 403 Varnish  b''
default UA  + garbage key  -> 403 Varnish  b''
custom UA   + valid key    -> 200 Heroku   b'[{"type_of":"article","id":4704524,...'
custom UA   + no key       -> 401 Heroku   b'{"error":"unauthorized","status":401}'
custom UA   + garbage key  -> 401 Heroku   b'{"error":"unauthorized","status":401}'
```

The left column is completely insensitive to the key. The right column is completely sensitive to it. That is the ordering, and it also explains the empty body: an edge rejection has nothing to say, because the code that writes helpful JSON errors lives downstream of it. A zero-length body on a 4xx is itself a signal. Applications explain themselves. Proxies hang up.

## What is actually on the blocklist

At this point I assumed it was a general "looks like a bot" heuristic, so I threw a spread of client strings at it to find the shape.

```
'python-urllib'           -> 403 Varnish
'urllib'                  -> 403 Varnish
'urllib3'                 -> 403 Varnish
'my-python-urllib-client' -> 403 Varnish
''                        -> 403 Varnish
'Java/17.0.1'             -> 403 Varnish

'python-requests'         -> 200 Heroku
'curl/8.4.0'              -> 200 Heroku
'Wget/1.21'               -> 200 Heroku
'okhttp/4.12.0'           -> 200 Heroku
'Go-http-client/1.1'      -> 200 Heroku
'scrapy/2.11'             -> 200 Heroku
```

It is not a bot heuristic. `scrapy` is a scraping framework and it sails through. `Wget` sails through. What gets stopped is a hand-picked list of substrings, and `urllib` is on it.

Then I checked the casing, mostly out of habit, and got the result that made me want to write this down:

```
urllib   -> 403        URLLIB   -> 200
Urllib   -> 200        urllib3  -> 403
uRllib   -> 200        URLlib3  -> 200
```

The match is case-sensitive. `urllib` is blocked and `Urllib` is not. One capital letter is the whole difference between a 403 and a 200.

## Why this lands on Python specifically

The practical damage is narrow and unlucky. Here are the real default User-Agent strings of the clients people actually use:

```
urllib (stdlib)   Python-urllib/3.14        -> 403
urllib3 direct    python-urllib3/2.2.1      -> 403
requests          python-requests/2.32.3    -> 200
httpx             python-httpx/0.27.0       -> 200
aiohttp           Python/3.14 aiohttp/3.9.5 -> 200
```

Two of five, and they are the two that ship lowest in the stack. If you reach for `requests` you never see this. If you write a script with no dependencies, which is exactly what you do when you are poking at an API for the first time, you get a bare 403 that says nothing and points at your credentials.

The fix is one line, and I want to be clear that it is a fix for my client, not a bypass of anything. The site publishes this API and issues me a key for it; what it declines to serve is an anonymous default string.

```python
HEADERS = {
    "api-key": KEY,
    "Accept": "application/vnd.forem.api-v1+json",
    "User-Agent": "MyApp/1.0 (+https://example.com/contact)",
}
```

Name your client. It costs nothing, it is what the header is for, and it means that when someone on the other end wonders who is hammering an endpoint, there is an answer.

## The part I want to keep

I spent about forty minutes on a credentials theory that the response had already ruled out. What I should have done first, and now do first, is read `Server`, `Content-Length`, and whether the body is machine-readable, before reading the status code's usual meaning.

A 403 does not mean "you lack permission." It means something returned 403. Which something is a different question, and the headers usually answer it before you have to guess.

```python
def where_did_this_come_from(e):
    return {"status": e.code,
            "server": e.headers.get("server"),
            "request_id": e.headers.get("x-request-id"),   # app layer sets this
            "body_len": len(e.read())}                     # 0 == edge, probably
```

`x-request-id` is the tell in the other direction. It is present on every 200 and absent on the 403, because the app assigns it and the app never saw me.

What is the longest you have spent debugging the wrong layer because the status code sounded like it was describing your problem? I want to hear the one where the header was sitting right there.
