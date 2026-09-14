# Measured in-session 2026-09-14 (M2 Pro). Source data for the 9/14–9/16 technical posts.

## A. aiscan detector probes
1-word doc "leverage" -> score 0 (ARTIFACT: degenerate input, misled first conclusion)
Padded to ~280 words:
  baseline 0 tells                  score 1  flags=1
  +1 plain leverage                 score 3  flags=2
  +5 plain leverage                 score 3  flags=2   <- dedup: 5 == 1
  +5 in FENCED code block           score 3  flags=2   <- code NOT stripped
  +5 in HTML COMMENT                score 3  flags=2   <- comments NOT stripped
  +5 in inline code                 score 3  flags=2

## B. make_barchart height (method: inject scrollHeight into document.title, chrome --dump-dom)
n    formula(210+76n)  real content   slack
1    286               288            -2   <- CLIPS
2    362               328            +34
3    438               402            +36
5    590               550            +40
8    818               772            +46
12   1122              1068           +54
20   1730              1660           +70
Real fit n>=2: height = 180 + 74n (exact on every measured n). Overshoot = 30 + 2n.

## C. make_cover title auto-shrink (420px card) — no overflow at any tested length
len 11/39/50/72/106 -> gap to footer 107/79/88/94/74 px. Heuristic is conservative but correct.

## D. Chrome render timing (6 covers)
single cover: 2.24-2.36s over 5 runs (fixed cost = process startup, not rendering)
sequential 6: 13.93s (2.32s each)
parallel   6:  3.86s (0.64s each)  -> 3.6x

## E. dev.to PUT /articles/{id} (verified on live id 4648628)
slug preserved after edit; edited_at 2026-09-14T08:35:06Z vs published_at 08:31:47Z (separate fields);
title lookup found the article on page 1 of me/published; body_markdown is FULL REPLACE, not patch.

## F. archive scan (68 posts)
mean 1.25, median 1.0, max 4, distribution {0:11, 1:35, 2:17, 3:4, 4:1}, PASS 63/68.
Same posts (dev.to API): 690 views, 3 reactions, 11 comments, 6 followers.
