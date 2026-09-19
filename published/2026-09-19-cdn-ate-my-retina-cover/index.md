<!--
REVIEW NOTES (delete before publishing), DO NOT PUBLISH until user says so.
- 9/19 HARDCORE 1/2. Measured today against live article 4671289.
  cover_image = media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/<urlencoded origin>
  origin PNG 1000x420, 207 KB. CDN serves webp, 70 KB (0.34x). Transform pins 1000x420 regardless of source.
  Separately verified --force-device-scale-factor=2 produces 2000x840 / 549 KB locally (2.8x bytes).
- Conclusion: a retina source cover is discarded by the transform. Good-faith credit to the commenter who suggested it.
-->

---
title: "A commenter told me to render retina covers. I measured what the CDN does with them."
published: false
description: "The tip was good and I almost shipped it. Then I looked at what dev.to actually serves: a fixed 1000x420 WebP, regardless of what I upload. The 2x source would have been 2.8x the bytes for an image nobody receives."
tags: webdev, performance, python, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-19-cdn-ate-my-retina-cover/cover.png
---

Someone left a useful comment on a post of mine about generating cover images with headless Chrome. Add `--force-device-scale-factor=2`, they said, and you get a high-DPI screenshot so your typography stays crisp on retina displays, instead of doubling the window size and fighting CSS transforms.

I tested it and it does exactly that:

```
default              : 1000x420px   194 KB
--force-device-scale-factor=2 : 2000x840px   549 KB
```

Sharper text, one flag, no CSS changes. I was ready to make it the default. Then I stopped, because I had never actually checked what the platform does with a cover after I hand it over.

## What the platform actually serves

The `cover_image` field on a published article does not point at my file. I pulled a live post and looked:

```
https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/
  https%3A%2F%2Fraw.githubusercontent.com%2F...%2Fcover.png
```

That is an image proxy with the transform baked into the path. `width=1000`, `height=420`, `fit=cover`, `format=auto`. My raw URL is the argument, url-encoded, at the end.

So the file I upload is an origin that gets fetched, transformed, and cached. Readers are served the output of that transform, never my PNG.

Fetching both tells you what the transform costs:

```python
import json, urllib.request, struct

a  = get_article(4671289)          # the live post
ci = a["cover_image"]              # the proxied URL

# pull the origin PNG my repo serves, read its dimensions out of the IHDR chunk
src = "https://raw.githubusercontent.com" + ci.split("raw.githubusercontent.com")[-1].replace("%2F", "/")
d   = urllib.request.urlopen(req(src)).read()
w, h = struct.unpack(">II", d[16:24])
print(f"origin PNG : {w}x{h}px, {len(d)/1024:.0f} KB")

# pull what a reader actually receives
cdn = urllib.request.urlopen(req(ci)).read()
print(f"CDN serves : webp, {len(cdn)/1024:.0f} KB")
print(f"ratio      : {len(cdn)/len(d):.2f}x the origin bytes")
```

```
origin PNG : 1000x420px, 207 KB
CDN serves : webp,        70 KB
ratio      : 0.34x the origin bytes
```

It is re-encoding to WebP and cutting the payload to a third. Good. That is a CDN doing its job.

It is also pinning the output to exactly 1000x420.

## Which kills the tip

`width=1000,height=420` is not a maximum, it is the transform. Hand it a 2000x840 source and it resamples down to 1000x420 and serves the same WebP it would have served from a 1000x420 source. The extra pixels are read once, at fetch time, and discarded.

So shipping the retina version would have meant:

- 2.8x the bytes in my repo, forever, for every post
- a slower origin fetch on first publish
- and zero difference in what any reader receives

The one case where it would matter is if dev.to ever changed that transform to emit a 2x variant for high-DPI screens, in which case a higher-resolution origin would suddenly pay off. Their proxy supports it, the parameters are right there in the URL. They just are not using it for cover images today.

## Why I nearly shipped it anyway

The tip was correct. It solves the problem it claims to solve: my local PNG really is sharper. I verified that part first and felt done, because the measurement I ran confirmed the change worked.

What I had not asked is whether the artifact I was improving is the artifact anyone consumes. It is not. There is a transform between my output and the reader, and it normalizes away the exact property I was optimizing.

That is the part worth taking apart, and it is not really about images. Measuring that your change worked is not the same as measuring that it reached anyone. I had a clean before-and-after on the wrong end of the pipeline, and a clean before-and-after is very convincing.

## What I actually changed

Nothing, for covers. The default stays 1000x420.

I did add a note in the generator, because the next person to read that comment will have the same good idea:

```python
# Cover images are re-transformed by dev.to's image proxy to exactly
# 1000x420 webp (see the width=/height= params in the cover_image URL),
# so a 2x render is thrown away. Keep 1x for covers.
# Inline images go through a different transform; 2x is worth testing there.
```

That last line is the follow-up I owe myself. Inline images in the body are hot-linked from my repo rather than passed through the cover transform, so the retina flag may genuinely help there. Different path, different answer, and I have not measured it yet.

If you publish images to a platform that proxies them, have you checked what the transform in the URL actually does? Mine was in plain text in a field I had been reading for weeks without parsing.
