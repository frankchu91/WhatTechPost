<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/15 HARDCORE 2/2. Measured today on an M2 Pro: single cover 2.24-2.36s (5 runs). 6 covers sequential 13.93s (2.32s each) vs parallel 3.86s (0.64s each) = 3.6x.
- The real insight: the cost is Chrome process startup, not rendering, so concurrency wins where a warm-process pool would be the "proper" fix but headless --screenshot is one-URL-per-process.
-->

---
title: "Every image my blog generates cost 2.3 seconds of Chrome boot. Six of them cost 14."
published: false
description: "I render every cover and chart by screenshotting HTML with headless Chrome. Timing it showed almost none of that time was rendering, and the fix was four lines and a 3.6x speedup."
tags: python, performance, webdev, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-15-parallel-chrome-3x/cover.png
---

I generate every cover image and chart on this blog by rendering a styled HTML page and screenshotting it with headless Chrome. It has been reliable for months and I never timed it, because each image appears in about the time it takes to alt-tab.

Then I generated a batch for three posts at once, noticed I was waiting, and actually measured.

```bash
for i in 1 2 3 4 5; do
  s=$(python3 -c "import time;print(time.time())")
  python3 scripts/make_cover.py --kicker "HANDS-ON" --title "Timing run" \
    --meta "x" --accent "#38bdf8" --out /tmp/t.png >/dev/null 2>&1
  e=$(python3 -c "import time;print(time.time())")
  python3 -c "print(f'cover run $i: {($e-$s):.2f}s')"
done
```

```
cover run 1: 2.35s
cover run 2: 2.35s
cover run 3: 2.36s
cover run 4: 2.24s
cover run 5: 2.25s
```

2.3 seconds, dead consistent, for a page with no images, no network requests, and about forty lines of CSS. Nothing in that document takes two seconds to lay out. The variance across five runs is 0.12s, which is the signature of a fixed cost rather than work that scales with the input.

The fixed cost is the process. Every call to my generator launches a whole browser, initializes it, opens one page, screenshots it, and tears the browser down. Rendering is a rounding error inside that.

## The obvious fix that headless Chrome will not give you

The correct answer to "process startup dominates" is a warm process: launch one browser, keep it alive, feed it pages. That is what Puppeteer and Playwright exist for.

But `--screenshot` is a one-shot flag. It takes exactly one URL, writes exactly one PNG, and exits. There is no way to hand a second file to the same process without moving to a driver library and the dependency that comes with it, which for a personal blog pipeline I did not want.

So the question becomes: if I cannot make the startup cheaper, can I stop paying for it serially?

## Four lines

```python
procs = []
for tmp, out in zip(tmp_files, out_paths):
    procs.append(subprocess.Popen([CHROME, "--headless", "--disable-gpu",
        f"--screenshot={out}", "--window-size=1000,420", "--hide-scrollbars", tmp],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
for p in procs:
    p.wait()
```

`subprocess.run` blocks until the process exits. `Popen` does not. Launch all of them, then wait for all of them. The startup cost still gets paid once per image, but the payments now overlap instead of queueing.

## What it bought

Six covers, same machine, same images, back to back:

```
sequential (6 covers, one Chrome launch each): 13.93s  (2.32s each)
parallel   (6 covers, launched concurrently):   3.86s  (0.64s each)
speedup: 3.6x
```

The per-image number dropping from 2.32s to 0.64s is the interesting part, because it is not a real per-image cost at all. It is the total divided by six. Six browsers starting at once do not each take 2.3 seconds of wall clock, they overlap and finish in under four.

3.6x rather than 6x is what you would expect: the machine has finite cores and six Chrome instances contend for them, so you recover most of the serialization and not all of it. On a three-post day with covers and charts that is roughly ten seconds of waiting turned into three.

## The part worth generalizing

I would have guessed, if asked, that image generation was slow because generating images is slow. It was not doing any image work worth measuring. It was paying a constant, and the constant was invisible because it was small enough to tolerate exactly once.

Constant costs hide inside loops. A 2.3-second startup feels instant when you trigger it by hand and feels like a broken pipeline when you trigger it six times. The measurement that found it was five lines of bash and I had gone months without running it, because nothing was failing.

Anyone running headless Chrome screenshots at real volume: did you end up moving to a driver with a warm process pool, or is spraying processes and waiting good enough at your scale? I am at "good enough" and curious where that stops being true.
