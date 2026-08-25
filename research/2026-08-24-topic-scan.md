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
- First open-weight model to crack top-3 dev power rankings (#2, 1674 Elo). #1 on Arena Frontend Code (1679) ahead of Claude Fable 5 (1631) and GPT-5.6 Sol (1618) — first Chinese model to top frontend coding. 2.8T MoE (104B active, 16/896 experts), 1M context, native vision, $3/$15 with 90% cache discount. Weights Jul 27.
- LICENSE verified 8/24 first-hand (huggingface.co/moonshotai/Kimi-K3 LICENSE file): custom "Kimi K3 License", NOT the modified-MIT of K2.x. MIT-style grant + (a) MaaS businesses over $20M revenue/12mo must sign separate agreement with Moonshot; (b) products >100M MAU or >$20M/mo revenue must display "Kimi K3" prominently in UI; internal use exempt. Moonshot's own materials say "open weight", never "open source". Draft corrected 8/24 — removed "fully open"/"no license ceiling" wording.
- Angle: open weights reached the actual frontier of a real leaderboard. Src: thenewstack · venturebeat · LogRocket · HF model card + LICENSE.

### Meta Muse Code (beta) + Spark 1.2 weights — VERIFIED 8/24, original claim was wrong
- CORRECTION: "modified Llama Community License" claim (llm-stats/release trackers) did NOT verify. No license has been published for Spark 1.2 — no date either. Zuckerberg quote: "Soon we'll also release the weights for Muse Spark 1.2, our latest foundation model." Constellation Research: "Muse Spark 1.2 has no publication date and no published license." businessmodelanalyst.com confirms; no source mentions a modified Llama license.
- Verified: Muse Code beta Aug 5 (terminal coding agent powered by Spark 1.2; macOS/Linux; $1.25/$4.25 per M tokens pay-as-you-go; discounted contributor tier = consent to data used for training — Alexandr Wang positioning on price). Muse Glimmer 30B: Apache 2.0 on Hugging Face, covers full-precision + quantized weights + DFlash drafter + perception encoder; no user gate/naming rule/AUP. Llama history for contrast: 700M-MAU threshold, "Built with Llama" naming rule, AUP. Muse Spark launched proprietary/cloud-only April 2026 (Llama retired).
- Post rewritten 8/24 around the verified story: the license line is blank; per-model license is a product decision; don't infer Spark 1.2's terms from Glimmer's. Src: constellationr.com · venturebeat.com (Glimmer Apache 2.0 piece + Muse Code piece) · businessmodelanalyst.com · techcrunch.com Aug 5.
