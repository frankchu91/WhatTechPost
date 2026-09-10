<!--
REVIEW NOTES (delete before publishing)
- FORMAT: practical/hands-on. First-hand: this is how scripts/make_barchart.py works (JSON spec -> HTML+CSS -> headless Chrome screenshot -> PNG). Real code, trimmed but accurate.
- Pairs with the 9/1 cover post (same HTML+Chrome engine). Cross-link it; reverse-link after publish.
- Non-obvious bit worth the post: fit output HEIGHT to the row count (covers are fixed-size, charts are not).
- Keep aiscan-clean; keep this comment free of the swap-table words too. No personal-take slot. NON-META. No AI-disclosure line. COVER: cover.png (HANDS-ON).
- DO NOT PUBLISH until the user says so (publish gate, 2026-09-08).
-->

---
title: "Charts for your README from a JSON spec, no charting library"
published: false
description: "You want a static bar-chart PNG in a README or a post. Chart.js needs a runtime, matplotlib looks off-brand. I render mine from JSON through headless Chrome, the same trick I use for cover images."
tags: webdev, css, python, showdev
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-08-charts-from-json-headless-chrome/cover.png
---

You want a bar chart in a README, or as an inline image in a blog post, or in a docs page. Somewhere that only takes a plain `<img>`. And every option is a little annoying. Chart.js draws to a canvas in a live browser, so getting a static PNG out of it is a chore. Matplotlib works but looks like matplotlib, and never matches your brand. A design tool gives you a one-off you cannot regenerate or diff.

I render mine from a JSON spec through headless Chrome, which is the same technique I already use to make [cover images from HTML and CSS](https://dev.to/frankchu/i-generate-every-blog-cover-with-headless-chrome-and-a-bit-of-css-no-design-tool-4hbe). One engine does covers and charts, both styled with CSS I control, both output as clean PNGs. Here is the whole thing.

## The spec

A chart is just data plus colors, so that is all the input is. A title, a list of series with a color each, and groups of values:

```json
{
  "title": "Request latency by tier (ms, lower is better)",
  "series": [{"name": "p50", "color": "#14b8a6"}, {"name": "p99", "color": "#64748b"}],
  "groups": [
    {"label": "cache hit",  "values": [40, 120]},
    {"label": "cache miss", "values": [380, 1173]}
  ]
}
```

![Bar chart titled 'Request latency by tier': cache hit shows low p50 and p99 bars, cache miss shows much longer bars](https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-08-charts-from-json-headless-chrome/demo.png)

That is the file I keep next to a post. It is readable, it lives in git, and regenerating the image after a number changes is one command instead of a trip back to a design tool.

## Turning it into bars

There is no chart library here. A bar is a `<div>` whose width is a percentage, and the only real work is normalizing every value against the largest one so the widths are proportional:

```python
gmax = max(v for g in spec["groups"] for v in g["values"]) or 1
for g in spec["groups"]:
    for i, v in enumerate(g["values"]):
        pct = 100 * v / gmax          # every bar relative to the biggest value
        bar = (f'<div class="bar" style="width:{pct:.1f}%;'
               f'background:{series[i]["color"]}"></div>')
```

The CSS is a few lines. Rounded rectangles, a fixed height, a small minimum width so a tiny value still shows something:

```css
.bar { height: 26px; border-radius: 6px; min-width: 2px; }
.val { font-family: ui-monospace, Menlo, monospace; color: #cdd8ea; }
```

Because it is CSS, the chart inherits the same dark background, the same accent colors, and the same font as my post covers, with no theming layer to keep in sync. When I want a different look, I change the stylesheet once.

## The one part that is not obvious

Covers are easy because they are a fixed size. Every cover I make is 1000 by 420, so I screenshot a 1000 by 420 page and I am done. A chart is not fixed. Two groups is a short image, eight groups is a tall one, and if you screenshot a fixed height you get either a band of dead space under a small chart or a cropped last bar on a big one.

So the height has to be computed from the data before the screenshot, not guessed:

```python
# header + legend is ~150px, each group ~76px, footer/padding ~60px
height = 150 + 76 * len(spec["groups"]) + 60
subprocess.run([CHROME, "--headless", "--disable-gpu",
    f"--screenshot={out}", f"--window-size=1000,{height}",
    "--hide-scrollbars", tmp], check=True)
```

That single line, deriving the window height from the number of groups, is the difference between a chart that always frames itself correctly and one you have to crop by hand every time. It took me two or three ugly exports to realize the sizing, not the drawing, was the actual problem.

## When to reach for this, and when not to

This is for simple, static, on-brand charts: bar charts in a README, a benchmark in a post, a number comparison in docs. Things that need to be a PNG and need to match everything around them. It is deliberately not a plotting library. If you need axes with real scales, scatter plots, time series, log axes, or anything interactive, use a proper charting tool and do not reinvent it in CSS.

But most charts I put in writing are four bars comparing two things, and for those the honest amount of tooling is a JSON file and a screenshot. No canvas runtime, no `pip install` of a plotting stack, no design tool, and the same rendering engine that already makes my covers. The chart at the top of a post and the cover behind it come out of one pipeline, and that is worth more to me than any single feature a real charting library would add.

If you generate images from HTML this way, or if you have a cleaner path from data to a static PNG, I want to see it, because the sizing problem alone tells me there are sharper approaches than mine out there.
