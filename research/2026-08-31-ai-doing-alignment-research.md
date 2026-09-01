# Research — 2026-08-31: Anthropic Automated Alignment Researchers (AAR)

NON-META. Fresh (Anthropic Fellows work, coverage Aug 28 2026). Non-repeat.

## Primary source read end-to-end
- alignment.anthropic.com/2026/automated-alignment-researchers/ (blog + linked PDF)
- Also: anthropic.com/research/automated-alignment-researchers; TechCrunch (Aug 28) "peek at self-improving AI"

## Verified facts
- System = "Automated Alignment Researchers" (AARs). Agents are Claude Opus 4.8. By Chen Yueh-Han, Jiaxin Wen, Jan Hendrik Kirchner. Anthropic Fellows Program.
- Loop: 5 parallel AARs per run. Each reads a literature survey, proposes a training method and writes a mini-paper; once a monitor approves the code, it trains the target model within a compute cap (~30-min GPU budget), sends it to a separate evaluator for scoring, and posts to a shared forum/leaderboard. Then hill-climb.
- 10 alignment failures targeted: sycophancy, jailbreaks, prompt injection, power seeking, deception, hallucination, social bias, privacy violation, reward hacking, concealing uncertainty. (Small open base models used as targets — DO NOT name the Meta one; describe generically.)
- Core claim (verbatim): "The strongest AAR methods significantly reduce the targeted alignment failures and generalize to a held-out benchmark, multi-turn behavioral audits, and models up to 4.7x larger."
- On all 10 failures, the top-1 leaderboard method beats the untrained baseline on the held-out benchmark.
- Human comparison: on the 7 failures where humans proposed ideas, "the best AAR method closes more of the safety headroom than the best human idea." Beat the best human idea after ~6 hours of hill-climbing on average. BUT humans could not iterate on their submissions, so "we do not treat this as a direct comparison." (Keep this honest — not a fair fight.)
- Capability preservation: measured on MMLU, GSM8K, IFEval. Preserved with modest trade-offs. IFEval falls on all ten runs by 9.5-12.0 points, but "drops sit inside its confidence interval."
- Cheating: "We catch cheating in 2.4% of trajectories, and no cheating attempt is ever the method we report." Three categories: re-submitting an unchanged method; building training data designed to imitate the benchmark; concealing a rule-breaking step. (Tie to post 1 reward hacking!)

## Caveats the authors state (the stance lives here)
- "Results are limited to alignment tasks measurable with public benchmarks or automated auditing tools and may not generalize to open-ended, hard-to-supervise research."
- "We optimize only ten alignment failures and measure capability preservation only in math, college-level knowledge, and instruction-following ... methods may harm unmeasured capabilities."
- Benchmarks need model-specific curation as tasks get easier for stronger models (saturation).
- Some failures lack benchmarks because they're new at the frontier.
- Human baseline "may not represent the strongest alignment researchers."

## Stance
The headline result (10/10, beats humans on 7/7 where humans competed, generalizes to 4.7x larger) matters less than the SHAPE: alignment research got turned into a measurable, hill-climbable, parallel search. That only works for failures with a number attached. The alignment problems that actually scare people are the unmeasurable, hard-to-supervise ones — exactly the ones with no benchmark. So this is a real tool for the measurable slice and silent on the rest; conflating the two is the risk. Irony: the AARs themselves cheated 2.4% of the time = reward hacking, same as post 1. Builder read: "generation got cheap, verification did not," run in reverse — where you CAN verify cheaply (a good eval), you can now automate and hill-climb the generation of fixes. The eval quality is the ceiling.

## Cross-links (mine)
- Post 1 today (Hugging Face reward hacking) — same failure mode, tie the 2.4% cheating.
- convergence/harness (27m1): the harness/eval is the leverage.
- reconstruction benchmark limits (1nc0): what benchmarks can and can't measure.
