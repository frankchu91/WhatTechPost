<!--
REVIEW NOTES (delete before publishing) — DO NOT PUBLISH until user says so.
- 9/24 HARDCORE 2/2. This retracts a number from my own published post. Measured today, same machine (M2 Pro, 12 cores), Chrome 154.0.8037.57.
  Published figure: 2.24-2.36s per render, 5 runs, "dead consistent", variance 0.12s.
  Today, 12 sequential runs: min 0.78s max 1.28s mean 0.93s stdev 0.164s; first run 1.28s vs rest 0.90s.
  Load average at time of measurement: 70.59 (I had just run concurrency experiments). 65% mem free.
  Also measured: unbounded parallel n=6 7.75s (1.29s/img), n=12 7.53s (0.63), n=24 14.00s (0.58);
  bounded pool(4) n=12 6.45s (0.54), n=24 13.46s (0.56). Bounded beat unbounded at n=12.
  No OOM kills observed, so the commenter's OOM claim is NOT confirmed on this box; the contention trend IS.
-->

---
title: "I published a benchmark. Two weeks later the same code ran 2.5x faster."
published: false
description: "Same machine, same script, same Chrome flags. I reported 2.3 seconds per render as a stable constant. Today it measured 0.93. The number wasn't wrong so much as it was never a constant."
tags: performance, testing, python, programming
cover_image: https://raw.githubusercontent.com/frankchu91/WhatTechPost/main/published/2026-09-24-my-benchmark-was-wrong/cover.png
---

Two weeks ago I published a timing measurement and called it a fixed cost. Five runs, 2.24 to 2.36 seconds each, variance of 0.12 seconds. I wrote that the tightness was "the signature of a fixed cost rather than work that scales with the input," and I built a whole argument on it.

Today, same machine, same script, same Chrome flags:

```
12 sequential runs: min 0.78s  max 1.28s  mean 0.93s  stdev 0.164s
first run 1.28s vs rest mean 0.90s  (cold-start effect: +0.37s)
```

0.93 seconds. Two and a half times faster than the number I published, from code I have not touched.

## What actually differed

Not the code. Not the Chrome version. The machine:

```
machine: Apple M2 Pro | cores 12
load:  70.59  35.02  17.73
```

A one-minute load average of 70 on a 12-core box. I had spent the previous ten minutes firing two dozen concurrent Chrome processes at it for a different experiment, and I took this measurement in the wake of that.

Which means neither number is the truth. The 2.3s I published was measured under whatever my machine happened to be doing that afternoon, and the 0.93s today was measured under a load spike I created myself. I reported the first one as a property of the software. It was a property of the afternoon.

## The tightness fooled me, and that is the interesting part

Here is what I got wrong conceptually, and I think it is a common error.

Five runs clustered inside 0.12 seconds looks like strong evidence. Low variance reads as a signal that you have isolated a real constant, and I said so explicitly in the post. But low variance within a sample tells you the conditions were stable **during that sample**. It says nothing about whether those conditions are the normal ones.

A tight cluster measured under a consistent-but-unrepresentative load is exactly as tight as a tight cluster measured under normal load. The spread cannot distinguish them. I treated precision as accuracy, which is the oldest measurement mistake there is, and I did it while writing a post about measuring things properly.

## What I should have recorded

The reading is not useless, it is just incomplete. A timing number without its conditions is not reproducible by anyone including me. The minimum I should have captured alongside it:

```python
import os, subprocess, time, statistics

def context():
    load1, load5, load15 = os.getloadavg()
    chrome = subprocess.run([CHROME, "--version"], capture_output=True, text=True).stdout.strip()
    return {"load_1m": round(load1, 2), "load_15m": round(load15, 2),
            "cores": os.cpu_count(), "chrome": chrome}

def timed(fn, n=12):
    xs = []
    for _ in range(n):
        t0 = time.time(); fn(); xs.append(time.time() - t0)
    return {"n": n, "min": min(xs), "max": max(xs),
            "mean": statistics.mean(xs), "stdev": statistics.pstdev(xs),
            "first": xs[0], "rest_mean": statistics.mean(xs[1:]),
            **context()}
```

Two details in there I would not have bothered with before. Reporting `first` separately from `rest_mean` surfaces cold start, which today was +0.37s and would have been invisible in a mean. And capturing `load_1m` at measurement time is the single line that would have caught this entire error, because a load average of 70 in the output would have stopped me publishing.

## The concurrency numbers, with the same caveat

The same session, measuring batch rendering:

```
unbounded parallel n=6    7.75s   1.29s/img
unbounded parallel n=12   7.53s   0.63s/img
unbounded parallel n=24  14.00s   0.58s/img
bounded pool(4)    n=12   6.45s   0.54s/img
bounded pool(4)    n=24  13.46s   0.56s/img
```

A reader who runs a screenshot service told me that spraying unbounded processes stops working past a few dozen renders, because memory contention makes that per-process constant unpredictable and something eventually gets OOM-killed. I did not reproduce an OOM kill on this box: all 24 renders succeeded in every configuration. But the direction supports him. At n=12 a bounded pool of four beat unbounded parallelism outright, 6.45s against 7.53s, which is the opposite of what "more concurrency is faster" predicts and exactly what contention looks like when it starts to bite.

I am not publishing those as constants either. They are one machine, one afternoon, one load profile.

## What I am changing

The post with the wrong number now carries a correction. Beyond that, I am not going to publish a timing figure again without the conditions attached, because a benchmark without its environment is not a measurement, it is an anecdote with decimal places.

And the general version, which cost me two public numbers to learn: **a tight cluster proves your conditions were stable, not that they were typical.** If you cannot say what the machine was doing while you measured, you do not know what you measured.

What is the most embarrassing benchmark you have had to retract? I would like company.
