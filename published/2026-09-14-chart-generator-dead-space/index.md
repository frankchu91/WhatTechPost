<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/14 HARDCORE 2/2. All numbers measured today. Method: inject scrollHeight into document.title, read it back with chrome --dump-dom.
- Real data: formula 210+76n vs measured content 180+74n (exact fit n>=2). Slack -2,+34,+36,+40,+46,+54,+70 at n=1,2,3,5,8,12,20. n=1 CLIPS by 2px.
-->

---
title: "My chart generator quietly padded every image with up to 70px of dead space"
published: false
description: "I render chart PNGs by screenshotting HTML, and I sized the window with a formula I guessed at months ago. I finally measured what the content actually needs. The formula was wrong at both ends."
tags: python, webdev, css, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-14-chart-generator-dead-space/cover.png
---

I generate the charts for my posts by rendering HTML and screenshotting it with headless Chrome. Covers are easy because they are a fixed size. A chart is not: two bars is a short image, twenty bars is a tall one, and the screenshot has to know the height before the browser has drawn anything.

So months ago I wrote this, eyeballed a few outputs, and never looked again:

```python
# fit window height to content: header ~170 + ~76 per group + brand/pad ~50
hgt = 150 + 76 * len(spec["groups"]) + 60
subprocess.run([CHROME, "--headless", "--disable-gpu",
                f"--screenshot={out}", f"--window-size=1000,{hgt}",
                "--hide-scrollbars", tmp], check=True)
```

Note the comment says 170 and 50 while the code says 150 and 60. That inconsistency is the smell. I guessed, adjusted until it looked fine, and shipped it.

## Measuring what the content actually needs

The hard part is that a screenshot cannot tell you whether content was clipped. The PNG is exactly the window size you asked for, always, so the output looks like confirmation no matter what.

The trick is to ask the browser instead. Inject a script that writes the real scroll height into the document title, then read the title back with `--dump-dom` instead of taking a picture:

```python
html = build_html(spec).replace(
    "</body>",
    "<script>document.title='H'+document.documentElement.scrollHeight</script></body>")
```

```bash
"$CHROME" --headless --disable-gpu --window-size=1000,200 \
  --dump-dom /tmp/chart.html | grep -oE '<title>H[0-9]+'
```

The window size in that call is deliberately tiny, because `scrollHeight` reports the full content regardless. Now I can compare what the content needs against what my formula hands it.

## The numbers

```
groups=1   formula=286    real_content=288    slack= -2 px
groups=2   formula=362    real_content=328    slack=+34 px
groups=3   formula=438    real_content=402    slack=+36 px
groups=5   formula=590    real_content=550    slack=+40 px
groups=8   formula=818    real_content=772    slack=+46 px
groups=12  formula=1122   real_content=1068   slack=+54 px
groups=20  formula=1730   real_content=1660   slack=+70 px
```

Two separate bugs, at opposite ends.

**At one group the image is clipped.** The content wants 288px and gets 286. Two pixels off the bottom, which is exactly enough to shave the brand line and not enough for me to notice in a year of looking at these.

**Everywhere else it overshoots, and the overshoot grows.** 34px of dead space at two groups, 70px at twenty. Every chart I have published has a band of empty background under it, getting worse the bigger the chart.

## The formula the data actually supports

Fit a line through the measured values for two groups and up:

```
slope     = (1660 - 328) / (20 - 2) = 74.0 px per group
intercept = 328 - 2 * 74            = 180
→ real height = 180 + 74n      # exact on every measured n >= 2
```

That is not approximate. Plug in n=12: 180 + 888 = 1068, which is the measured number to the pixel. My formula was `210 + 76n`, so I was overshooting by `30 + 2n` every single time. Both constants were wrong, and the per-row error compounded.

The one group case sits off the line at 288 rather than the predicted 254, because the title and legend block has a minimum height that dominates when there is almost no content under it.

```python
# measured, not guessed
hgt = 288 if len(spec["groups"]) == 1 else 180 + 74 * len(spec["groups"])
```

## What I actually take from this

The generator never failed. No exception, no warning, no obviously broken image. It produced a slightly-too-tall PNG a hundred times and a two-pixel-clipped one occasionally, and because the screenshot always matches the window you requested, the output could not tell me I was wrong. The only way to find it was to measure the thing I had been assuming.

The cheap version of that lesson: when your code has a magic constant and a comment that disagrees with it, the constant is a guess, and the guess is probably wrong in a way nothing will ever report.

What is your version of this, the magic number that has been quietly slightly wrong in production for months? I want the ones that never threw an error.
