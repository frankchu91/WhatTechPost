<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/27 HARDCORE 2/2. Measured today against media2.dev.to's image proxy.
  Source: a real 1000x420 PNG from my own repo, 211618 bytes.
  Output dimensions parsed straight out of the returned WebP (VP8/VP8L/VP8X headers), not assumed:
    width=1000,height=420,fit=cover       -> 1000x420  71664B
    width=800,height=,fit=scale-down      ->  800x336  46168B
    width=800,height=200,fit=cover        ->  800x200  35624B   <- crops
    width=800,height=200,fit=scale-down   ->  476x200  23946B   <- fits inside
    width=400,height=400,fit=cover        ->  400x400  22970B   <- square crop of a banner
    width=400,height=400,fit=scale-down   ->  400x168  20226B
    width=4000,height=,fit=scale-down     -> 1000x420  71664B   <- never upscales
    width=4000,height=1680,fit=cover      -> 1000x420  71664B   <- never upscales
  Everything comes back image/webp regardless of source format (source was PNG).
-->

---
title: "dev.to re-encodes and crops your cover image, and I measured exactly where the crop lands"
published: false
description: "Covers go through fit=cover, inline images through fit=scale-down. One of those throws pixels away. I parsed the returned WebP headers to find out which pixels."
tags: webdev, images, performance, python
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-27-devto-crops-your-cover/cover.png
---

I had a cover image with a line of small text near the left edge. On the post page it looked right. In the feed card it was gone. Not clipped, not small, absent, and I could not reproduce it by resizing my browser.

The image you see on dev.to is not the image you uploaded. It comes through a transform proxy, and the parameters in the proxy URL decide what happens to your pixels. There are two different parameter sets in play depending on where the image appears, and they behave in opposite ways.

## Reading the actual output

I did not want to eyeball this, so I parsed dimensions out of the bytes that came back. Everything the proxy returns is WebP, whatever you sent it, and WebP stores its size in one of three container variants:

```python
import struct

def webp_size(b):
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        return None
    fmt = b[12:16]
    if fmt == b"VP8X":                       # extended
        w = int.from_bytes(b[24:27], "little") + 1
        h = int.from_bytes(b[27:30], "little") + 1
        return w, h
    if fmt == b"VP8 ":                       # lossy
        i = b.find(b"\x9d\x01\x2a")
        return (struct.unpack("<H", b[i+3:i+5])[0] & 0x3FFF,
                struct.unpack("<H", b[i+5:i+7])[0] & 0x3FFF)
    if fmt == b"VP8L":                       # lossless
        n = int.from_bytes(b[21:25], "little")
        return (n & 0x3FFF) + 1, ((n >> 14) & 0x3FFF) + 1
```

The source is one of my own covers, a 1000x420 PNG at 211,618 bytes. Every row below is a real fetch.

```
transform requested                            returned      bytes
width=1000,height=420,fit=cover                1000x420      71664
width=800,height=,fit=scale-down                800x336      46168
width=800,height=200,fit=cover                  800x200      35624
width=800,height=200,fit=scale-down             476x200      23946
width=400,height=400,fit=cover                  400x400      22970
width=400,height=400,fit=scale-down             400x168      20226
width=4000,height=,fit=scale-down              1000x420      71664
width=4000,height=1680,fit=cover               1000x420      71664
```

Three behaviours fall straight out of that table.

`fit=cover` returns exactly the box you asked for. A 1000x420 banner requested at 400x400 comes back as a 400x400 image, and since the source is not square, that is a crop. Roughly 58% of the width is thrown away and nothing warns you.

`fit=scale-down` preserves the aspect ratio and fits the whole image inside the box. The same 400x400 request returns 400x168, letterboxed rather than cropped.

Neither mode will upscale. Asking for 4000 wide returns the source's 1000, in both modes. So a small source stays small and gets displayed stretched by CSS, which is the other way covers end up looking wrong.

## Which mode applies where

The parameters are not yours to choose. They are baked into the URL the platform generates, and the two contexts use different ones:

```
cover  : width=1000,height=420,fit=cover,gravity=auto,format=auto
inline : width=800,height=,fit=scale-down,gravity=auto,format=auto
```

Read those carefully, because the authoring rules they imply are opposites.

The cover has a fixed height and crops. Your cover must be 1000x420, or close to that ratio, or the proxy decides what to discard. `gravity=auto` means the crop is centred by a heuristic rather than by you. That was my missing text: content near the edge of a banner whose ratio did not match.

The inline transform has an empty height and scales down. There is no crop and no vertical constraint at all, so the only thing that matters for an inline chart or screenshot is that it is at least 800 pixels wide. Height is free. A tall, narrow diagram is fine inline and would be destroyed as a cover.

## The size side of it

The re-encode is doing real work:

```
origin PNG                        211618 B   1000x420
proxy  WebP, same dimensions       71664 B   1000x420    -66%
proxy  WebP, 800 wide              46168 B    800x336    -78%
```

Two thirds off at identical dimensions. That is WebP against a PNG I generated from HTML with a headless browser, so it is a favourable case, but it does mean there is no point hand-optimising the file you commit. The proxy re-encodes everything anyway and your careful PNG crunching is discarded. What the source file needs to be is large enough and the right shape; its bytes do not survive.

## What I do now

Generate covers at exactly 1000x420 and keep anything meaningful inside a safe area, away from the edges, because `gravity=auto` gets to move the frame and I do not know its rules. Generate inline images at 1600 wide for retina, any height, and stop caring about file size. And when an image looks wrong in one place and right in another, fetch both URLs and measure the bytes rather than squinting at a browser.

```python
import urllib.request

def check(url):
    b = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "MyApp/1.0"})).read()
    return webp_size(b), len(b)
```

Four lines, and it would have answered in a minute a question I stared at for considerably longer.

If you publish on a platform that transforms your images, do you know which fit mode it uses? I had been on this one for three months and assumed, incorrectly, that a cover was scaled rather than cropped.
