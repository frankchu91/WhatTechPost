# Switchyard hands-on — 2026-08-13

Machine: M2 Pro 32GB, ollama 0.32.7. Installed: nemo-switchyard 0.2.0 via uv tool.

## Install gotchas (all real, hit in order)

1. README/docs say `uv tool install --python 3.10 "nemo-switchyard[cli]"` — fails: package requires Python >=3.12. Works with default (3.13).
2. `switchyard serve` → `ModuleNotFoundError: No module named 'yaml'` — [cli] extra missing pyyaml.
3. After adding pyyaml → `No module named 'uvicorn'`. Fix that installed everything: `uv tool install --force --with pyyaml --with uvicorn --with fastapi "nemo-switchyard[cli]"`.

## Config discovery

- Docs describe TOML for launch/standalone-Rust paths; `serve` takes a YAML "route bundle" that is undocumented — schema reverse-engineered from installed source (`cli/route_bundle.py`): top-level `{routes: {<id>: {type: ..., ...}}}`; route types: model, random_routing, deterministic, escalation_router, stage_router(?).
- escalation_router keys: weak/strong/judge (LlmTarget: model, base_url, api_key, ...), fallback_target_on_evict, tier_timeout_s, session_key_depth, affinity_*. Judge tuning (judge_min_turn=3, judge_escalate_confirmations=2) NOT exposed in YAML — defaults fixed.
- Working config: routes.yaml with weak=llama3.2:3b, strong=qwen3:14b, judge=llama3.2:3b, all via http://localhost:11434/v1.

## Measurements

- /v1/models exposes route as a "model" (id=local, profile=escalation_router, streaming+tools capabilities advertised).
- First proxy call: 3.78s vs 0.22s direct (one-time warmup). Warm: proxy [0.30, 0.18, 0.18]s vs direct [0.18, 0.16, 0.18]s → overhead ≈ 0-0.1s.
- Simple Q "2+2" → routed to weak (llama3.2:3b), `model` field in response confirms.
- 4-turn moderately-hard conversation: no escalation (all 3B).
- 7-turn escalating-difficulty conversation (lock-free MPMC queue → hazard pointers → linearizability proof → TLA+): turns 1-6 on llama3.2:3b (1.8-3.8s), **turn 7 escalated to qwen3:14b** (21.0s). One-way latch per session-affinity design. /v1/stats shows both models with token accounting.

## Post angle

Continuity: bench post concluded "route local models like API models" → NVIDIA productized exactly that (same week). Story: 3 packaging bugs → undocumented YAML → it actually works, judge-latched escalation fired on turn 7, ~zero warm overhead, all local, all free.
