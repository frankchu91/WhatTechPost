# Topic scan — 2026-08-12

## Picked: Meta Muse Glimmer (Aug 10) → drafts/2026-08-22

- 30B multimodal, distilled from Muse Spark, Apache 2.0, tuned for always-on local agent workflows. On HF org `meta-models` since Aug 10.
- Full precision >55GB. Two official 4-bit quants: 32GB-VRAM K-Quant-Dynamic (claimed 0.2% degradation); 17GB K-Quant for 24GB cards (claimed 1.0%).
- DFlash block-level speculative decoding: RTX 5090 74.9→233.4 tok/s (3.1x); M4 Max 23.7→37.8; M5 Max 26.6→50.2.
- Self-reported benchmarks: MCP Atlas 75.5, SWE-Bench Pro 51.2, AIME 2026 94.7, Charxiv 78.8, DeepSearch QA 74.6, Gaia2 43.3.
- VERIFIED by us on HF (2026-08-12): meta-models/Muse-Glimmer-30B + -GGUF exist; community quants already up (unsloth, bartowski GGUF; mlx-community 4bit + bf16 for Macs; AWQ-INT4). ~203 search results on HF.
- Coverage: https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now · https://www.marktechpost.com/2026/08/10/meta-ai-releases-muse-glimmer/ · https://aiweekly.co/alerts/meta-ships-muse-glimmer-30b-as-local-agent-model-on-consumer-gpus

## Candidates for next cycles

- **Cloudflare Kitesurf** (Aug 7): browser built for agents on Workers; Rust→WASM; Blitz renderer + Stylo CSS + Boa JS; CDP-compatible (Playwright/Puppeteer). Perf vs Chromium: screenshots 380ms/57.8MiB vs 1173ms/271MiB; HTML extraction 229ms/39.4MiB vs 877ms/273.7MiB. Free beta via Browser Run. https://techcrunch.com/2026/08/07/cloudflare-launches-kitesurf-a-browser-built-for-ai-agents/
- **Qwen3.8 weights follow-up**: still not on HF as of Aug 12 despite "week of Aug 10" promise; license still undisclosed; prior Qwen releases used Tongyi Qianwen license (100M MAU clause). Natural follow-up to our Aug 12 post if the drop happens (or keeps not happening). https://byteiota.com/qwen3-8-open-weights-drop-this-week-read-before-you-download/
- GPT-5.6-Cyber (Aug 10, security-focused) — needs more research.
- Seedance 2.5 (ByteDance, Aug 8) / Qwen Image 3.0 Pro — gen-media beat, off-lane unless tied to a build.
- Amazon renamed Bedrock Agents → "Classic", closed to new customers (platform churn angle).
