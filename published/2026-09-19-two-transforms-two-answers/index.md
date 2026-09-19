<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/19 HARDCORE 2/2. Measured today.
  COVER transform:  width=1000,height=420,fit=cover,gravity=auto,format=auto   (both dims pinned)
  INLINE transform: width=800,height=,fit=scale-down,gravity=auto,format=auto  (height empty, scale-down)
- fit=cover with both dims = fixed output, crops to fill. fit=scale-down + open height = never upscales, preserves aspect.
- Consequence: identical source, opposite advice. Covers must be authored AT 1000x420. Inline images must be authored >= 800 wide and are free to be taller.
-->

---
title: "Same platform, two image transforms, opposite rules for how to author them"
published: false
description: "I assumed one image pipeline. There are two, with different parameters, and they disagree about resolution, aspect ratio, and whether your extra pixels survive. Here's how to read the transform out of the URL."
tags: webdev, performance, programming, css
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-19-two-transforms-two-answers/cover.png
---

I generate every image on my blog, covers and inline charts, from the same HTML-to-screenshot pipeline. I had been treating them as one problem with one set of rules.

They are two problems. The platform runs each through a different transform, and once I read the parameters, the correct authoring advice for the two turns out to be opposite.

## Reading the transform out of the URL

Both go through the same image proxy, and the proxy puts its entire configuration in the path. That means you can read exactly what will happen to your file without any documentation.

The cover, from the `cover_image` field of a live post:

```
media2.dev.to/dynamic/image/
  width=1000,height=420,fit=cover,gravity=auto,format=auto
  /https%3A%2F%2Fraw.githubusercontent.com%2F...%2Fcover.png
```

An inline image, from the rendered `body_html` of another post:

```
media2.dev.to/dynamic/image/
  width=800,height=,fit=scale-down,gravity=auto,format=auto
  /https%3A%2F%2F...
```

Both came straight out of the API, no guessing:

```python
import re

a = get_article(ARTICLE_ID)

# the cover transform lives in the cover_image field
cover_params = a["cover_image"].split("/dynamic/image/")[1].split("/")[0]

# the inline transform only appears in the RENDERED html, not in body_markdown
inline_src   = re.findall(r'<img[^>]+src="([^"]+)"', a["body_html"])[0]
inline_params = inline_src.split("/dynamic/image/")[1].split("/")[0]

print("cover :", cover_params)
print("inline:", inline_params)
```

```
cover : width=1000,height=420,fit=cover,gravity=auto,format=auto
inline: width=800,height=,fit=scale-down,gravity=auto,format=auto
```

Note where each one hides. The cover transform is in a top-level field you can read
directly. The inline transform exists only in `body_html`; `body_markdown` still holds
your original raw URL, so if you only ever look at the markdown you will never know a
proxy is involved at all.

Three differences, and every one of them changes what you should hand it.

## `fit=cover` with both dimensions

The cover transform pins width and height. `fit=cover` means fill that exact box and crop whatever does not fit, with `gravity=auto` choosing the crop.

Consequences:

- Output is always 1000x420 regardless of input. A higher-resolution source is resampled down and the extra pixels are discarded, which is why rendering covers at 2x device scale buys nothing.
- Aspect ratio is not preserved, it is enforced. Hand it a square and it crops to 1000x420. Anything important near an edge is at the mercy of an automatic gravity heuristic.

So the rule for covers: author at exactly 1000x420, and do not put anything that matters near the edges.

## `fit=scale-down` with an empty height

The inline transform is a different animal. `height=` is empty, so only width is constrained, and `scale-down` means it will shrink an image that exceeds the limit and **never enlarge** one that does not.

Consequences:

- A 400px-wide chart is served at 400px. It is not stretched to 800. If your source is narrower than the limit, you shipped a small image and the proxy will not save you.
- Aspect ratio is preserved, because only one dimension is constrained. A tall chart stays tall.
- A source wider than 800 is scaled down, so the extra width is discarded, but the *height* comes along proportionally.

So the rule for inline images: author at **at least** 800 wide, and let height be whatever the content needs.

## The two rules side by side

| | cover | inline |
|---|---|---|
| transform | `width=1000,height=420,fit=cover` | `width=800,height=,fit=scale-down` |
| output size | always 1000x420 | width capped at 800, height free |
| too small a source | upscaled, blurry | served small, no upscale |
| too large a source | wasted bytes | width wasted, height preserved |
| aspect ratio | cropped to fit | preserved |
| author it at | exactly 1000x420 | ≥ 800 wide, any height |

The row that matters most is the last one, and I had a single rule where I needed two.

It also resolves something from my chart generator. That tool computes output height from the number of rows, so a twenty-row chart comes out 1660px tall. Under the cover transform that would be crushed into a 420px box and cropped to uselessness. Under the inline transform the height survives untouched, because height is unconstrained. My tall charts were only ever fine because they happen to go inline, not because I designed for it.

```python
COVER_W, COVER_H = 1000, 420    # fit=cover pins both; author exactly
INLINE_MIN_W     = 800          # fit=scale-down never upscales; author >= this
```

## The habit worth stealing

A URL-based image proxy is self-documenting if you read it. The parameters are sitting in the path of every image on the page, and they tell you the resize mode, the target dimensions, the crop behavior, and the format policy, without asking anyone.

I had been looking at that string for weeks as an opaque prefix before my real URL. Ten seconds of parsing it would have told me that my two image types had two different contracts, and saved me from nearly shipping a change that optimized for a transform that does not apply.

If your platform proxies images, go read one of its URLs. What are the actual parameters, and does your generator author to them, or to what you assumed?
