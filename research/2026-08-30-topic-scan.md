# Topic scan — 2026-08-30 (3 drafts, per-post folders, NO META)

Ng piece already published today. These 3 are non-Meta, non-repeat.

## Verified facts

### OpenHands (open autonomous coding agent)
- MIT-licensed, open source (formerly OpenDevin). ~70K GitHub stars. $18.8M Series A. Contributors from AMD/Apple/Google/Amazon/Netflix/NVIDIA.
- Given a GitHub issue or task, plans + executes the whole solution WITHOUT per-step direction, in a sandboxed Docker env (terminal, editor, browser, filesystem): writes code, runs terminal commands, browses docs, calls APIs, runs tests, debugs, iterates, opens PRs. 72% SWE-Bench (at/above proprietary alternatives). openhands.dev.
- Angle: open coding agents caught up to closed; the "issue in, PR out, unsupervised in a sandbox" model; the real question becomes review/trust, not capability. Src: openhands.dev · theaiagentindex · vibecoding.

### DeepSeek V4-Pro GA (build 0813, Aug 12-13)
- Flagship leaves preview: 1.6T total / 49B active, 1M context, up to 384K output. Agent-focused. New low/high/max "thinking effort" selector.
- PRICING (counter-trend): DeepSeek RAISED prices Aug 17. Pro ~$1.32 in / $3.96 out at PEAK (up from a flat ~$0.87 out). Off-peak = half price. Cache hits ~97% discount. Flash $0.44/$1.32.
- Angle: two hooks — (1) the effort selector (matches the escalation/routing theme), (2) DeepSeek RAISING prices in the middle of a price war, and time-of-day pricing + huge cache discount. What a price increase signals. Src: unite.ai · api-docs.deepseek.com/news/news260813 · digitalapplied.

### The two-agent coding stack (trend)
- Common Aug 2026 stack: frontier terminal agent (Claude Code or Codex) for heavy multi-file work + a FREE open-source agent (OpenCode, Cline) for lower-stakes tasks, connected through MCP servers.
- Angle: routing at the HUMAN level — you run two agents, not one, and pick per task. Practical daily-driver piece; ties routing/harness/MCP themes but concrete. Real tools only (Claude Code, Codex, Cline, OpenCode, MCP). No hard facts needed beyond naming them.
