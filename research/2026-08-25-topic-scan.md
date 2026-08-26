# Topic scan — 2026-08-25 (3 NEW topics, replacing harness/Kimi/Meta plan)

Note: harness-rankings + Kimi K3 already LIVE (published 8/25). Meta Muse shelved (user chose 3 new topics). These 3 are fresh.
WRITE TO PASS aiscan: em-dashes single digits, bold <=2, no hollow intensifiers.

## Facts (verified 2026-08-25)

### MCP 2026 roadmap (published ~Aug 23 analysis)
- Five priorities: (1) agentic messaging primitives — server-initiated events, maturing the Tasks extension (async/long-running); (2) HTTP-native transport unification — Google-proposed STATELESS transport so servers scale on Cloud Run/K8s (today's streamable HTTP is stateful, hard to scale); (3) agent identity & enterprise security — DPoP, Workload Identity Federation, token exchange, delegation to sub-agents; (4) progressive tool discovery — reveal tools gradually instead of loading hundreds into context; (5) better SDK DX.
- Shift: from "tool-calling standard" to "production connectivity layer" for agents at scale. Src: modelcontextprotocol.io/development/roadmap · vktr.com · nxcode.io · toloka.ai.

### NVIDIA Groq 3 LPX — full production (Hot Chips 2026, Aug 24)
- NVIDIA completed ~$20B deal (Dec 24, 2025) to acqui-hire Groq: senior staff, physical assets, NON-EXCLUSIVE license to Groq's LPU (Language Processor Unit). 
- Groq 3 LPX = dedicated inference accelerator, entered FULL PRODUCTION Aug 2026; slots into Vera Rubin NVL72 racks (dedicated LPX racks, up to 256 LPX/rack); targets low latency in the DECODE phase of inference; "fastest token generation ever recorded" (vendor). 
- Angle: inference is now its own silicon battleground; NVIDIA absorbed the LPU challenger. Ties to Ultrafast/Cerebras thesis (differentiation moving into inference/serving). Src: siliconangle.com/2026/08/24 · servethehome.com · blogs.nvidia.com · nvidia.com/data-center/lpx.

### Thomson Reuters 'Thomson' LLM (Aug 24)
- First proprietary LLM; built from an open-source base with mid/post-training on decades of Westlaw, Practical Law, Checkpoint, Reuters content. Fully owned/controlled by TR. $40M total program (talent+compute); FINAL TRAINING RUN for the launched version cost just $450,000. First deployment: CoCounsel Legal (Tabular Analysis).
- Angle: the data-moat play — you can't out-general the frontier, but owning decades of proprietary domain content lets you build a vertical frontier model cheaply. $40M program / $450K final run is the striking contrast. Src: thomsonreuters.com press release · artificiallawyer.com · siliconangle.com/2026/08/24 · lawnext.com.
