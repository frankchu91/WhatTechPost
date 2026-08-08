# Topic scan — 2026-08-07

Sources collected during first candidate scan (web search, Aug 7 2026).

## 1. NVIDIA NOOA (open-sourced this week)

- Agents as a single Python class: methods = actions, fields = state, docstrings = prompts, type annotations = enforced contracts. Method body `...` → completed by LLM loop; normal body → deterministic Python.
- 253-line agent: 82.2% SWE-bench Verified (GPT-5.5 xhigh); 86.8% CyberGym L1 (top open-source result).
- Security note: can execute LLM-generated Python — sandbox required (NVIDIA OpenShell).
- Repo: https://github.com/NVIDIA-NeMo/labs-OO-Agents · Paper: https://arxiv.org/abs/2607.20709
- Coverage: https://www.marktechpost.com/2026/08/07/nvidia-ai-releases-nooa-an-object-oriented-python-framework/ · https://thenewstack.io/nvidia-nooa-agent-framework/

## 2. API price war

- Jul 30: OpenAI cut GPT-5.6 Luna 80% ($1/$6 → $0.20/$1.20), Terra 20% ($2.50/$15 → $2/$12), Sol unchanged ($5/$30).
- Claude Sonnet 5 intro $2/$10 reverts to $3/$15 on Sep 1. Opus 5: $5/$25.
- Coverage: https://venturebeat.com/technology/ai-price-wars-openai-cuts-gpt-5-6-luna-prices-by-80-as-model-competition-shifts-toward-cost · https://www.unite.ai/openai-cuts-api-prices-on-its-two-cheaper-gpt-5-6-tiers/ · https://www.digitalapplied.com/blog/ai-api-pricing-august-2026-cuts-promos-tracker

## 3. Qwen3.8-Max (Aug 3)

- 2.4T MoE, 1M context. API $2/$6, $0.25 cached input per 1M.
- Claims: OSWorld-Verified 86.1 vs GPT-5.6 Sol Max 83.2 and Fable 5 85.0; Terminal-Bench 2.1 86.6 (between Sol 88.8 and Opus 4.8/Fable 5 84.6); top PaperBench score.
- Open weights promised "next week" incl. Qwen3.8-27B; license undisclosed.
- Coverage: https://venturebeat.com/technology/qwen3-8-max-arrives-with-a-bold-claim-it-outperforms-gpt-5-6-sol-max-and-fable-5-on-agentic-computer-use · https://www.marktechpost.com/2026/08/03/alibaba-qwen-releases-qwen3-8-max/ · https://www.latent.space/p/ainews-qwen-38-max24t-and-27b-new

## 4. OpenAI Astra math proofs (Aug 1)

- 10 problems open 10+ years; 249-page manuscript + Lean 4 certificates on GitHub, Apache 2.0, zero `sorry`.
- ~$2,000 token cost at Sol rates. Headline: explicit non-sofic group construction (open since Gromov 1999); disproved Connes rigidity conjecture. No Millennium Problems.
- Model unreleased; results under independent examination via published proofs.
- Coverage: https://siliconangle.com/2026/08/02/openais-astra-solves-10-long-open-math-problems-publishes-proofs/ · https://www.implicator.ai/openai-astra-10-math-problems-lean-proofs/ · https://www.datacamp.com/blog/open-ai-model-astra-solved-ten-open-math-problems

## 5. Coding-agent convergence

- Terminal-Bench 2.1: GPT-5.6 Sol 89.5% vs Claude Opus 5 (max effort) 89.1% — within half a point.
- Context: Opus 5 at half flagship price; Claude Code shipped terminal security scanner; open weights cheap enough to run coding agents "for cents".
- Coverage: https://www.buildfastwithai.com/blogs/7-ai-tools-changed-developer-workflow-augustt-2026 · https://www.morphllm.com/best-ai-coding-agents-2026 · https://www.developersdigest.tech/blog/what-hacker-news-gets-right-about-ai-coding-agents-2026

## Also seen, not shortlisted

- Demis Hassabis stepping out of DeepMind CEO role (Aug 6, Bloomberg) — industry news, weak builder angle.
- GLM-5.2 (Z.ai) 1M-context agentic model; Kimi K3; Meta Muse Spark 1.2 (Aug 5) — candidates for next cycles.
- Suno tightening download limits after streaming-fraud abuse (music, off-beat for this account).
- Sinch Agent Tools launch (Aug 4) — vendor PR, skip.
