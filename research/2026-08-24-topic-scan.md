# Topic scan — 2026-08-24 (3/day, 8/24-8/25)

## Schedule
- 8/24: Anthropic protein binders · Cognition $40B / agent funding · Reconstruction benchmark
- 8/25: CellCog harness rankings · Kimi K3 open-weight #1 · Meta Muse Code + Spark 1.2 weights

## Facts (verified 2026-08-24)

### Anthropic — Claude autonomous protein design (Aug 20)
- Claude models (Mythos Preview, Opus 4.8) autonomously designed de novo protein binders, lab-validated by Adaptyv Bio + Twist Bioscience.
- 354 confirmed binders from 1,320 designs across 15 targets; succeeded on 14/15. Hit rates: Mythos Preview 26.7%, Opus 4.8 22.6% (48h); Mythos 35.1% on single-target 24h sessions. Industry typical 10-15%.
- RBX1 target: Mythos 40% hit rate vs 3.7% among human competition participants. Some designs bound several times tighter than best published.
- Opus 5 separately processed raw NMR/LC-MS data in 23/19 min, purity within 0.1% of lab reading.
- Angle: generate-then-verify at scale in the physical world (thousands of candidates → wet-lab filter → survivors). Same shape as the Astra/Lean post. Src: anthropic.com/research/Claude-accelerates-protein-design · techtimes/dataconomy Aug 20.

### Cognition $40B + agent funding surge (Aug 12-13)
- Cognition (Devin) in talks at $40B, <3 months after $1B raise at $26B. $1B annualized-revenue-run-rate target ($492M three months ago); enterprise Devin usage +50% MoM for 6 months. Clients: Mercedes-Benz, NASA, Goldman Sachs.
- Broader: ~$633M reported agent funding in first ~12 days of August (≈ a full July); HappyRobot $150M@$1.2B, Zenity $125M. VCs backing agents that do measurable work, not chatbot wrappers. Src: techcrunch Aug 12 · the-agent-report.

### Reconstruction benchmark (arXiv 2608.16645, Aug 2026)
- Blind, anti-leakage benchmark: recover research ideas from pre-publication bibliographies. Frontier LLMs single-model: 3-15%. Reference-only multi-agent (cross-model review + Swiss tournament, no web): ~23-42% across 6 domains, ~2.4x lift. 7 models, 643 papers, ML + 5 Nature-family domains.
- Angle: honest limits — genuine novel-idea generation is still hard; multi-agent helps but doesn't solve. Counter-hype. Src: arxiv.org/abs/2608.16645 · techtimes Aug 19.

### CellCog agent-harness rankings (Aug 2026)
- Claude Code #1 for depth of hooks, subagents, dynamic workflows; default for long autonomous coding. Codex CLI for cloud/PR-shaped autonomy. Cursor leads in-editor. Claude Code on Opus 5 (near-flagship at half price, per-request effort dial, per-subagent model control).
- Angle: someone's ranking HARNESSES now, not just models — the harness is the product. Ties to my convergence post. Src: aiagentstore / LogRocket power rankings Aug 2026.

### Kimi K3 (Moonshot) tops open-weight dev rankings
- First open-weight model to crack top-3 dev power rankings (#2, 1674 Elo). #1 on Arena Frontend Code (1679) ahead of Claude Fable 5 (1631) and GPT-5.6 Sol (1618) — first Chinese model to top frontend coding. 2.8T MoE, 1M context, native vision, $3/$15 with 90% cache discount. Full open weights Jul 27.
- Angle: open weights reached the actual frontier of a real leaderboard. Src: thenewstack · venturebeat · LogRocket.

### Meta Muse Code (beta) + Spark 1.2 weights
- Meta Superintelligence Labs released Muse Code (beta) + Muse Spark 1.2; Spark 1.2 weights to be open-sourced under a MODIFIED Llama Community License (not Apache). Muse Glimmer 30B already shipped Apache 2.0.
- Angle: Meta's open-source coding push, but the license nuance matters — apply the open-weights checklist. Src: llm-stats / release trackers Aug 2026. VERIFY license specifics before publishing.
