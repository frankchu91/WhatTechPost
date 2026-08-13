#!/usr/bin/env python3
"""Benchmark local models on agent-relevant tasks via ollama.

Tests per model:
  1. speed     — prompt-processing and generation tok/s (warm), incl. a ~1k-token
                 prompt to simulate agent context re-reads
  2. json      — strict constrained-JSON completion x5: valid? schema-conformant?
                 how many tokens burned on thinking?
  3. tools     — ollama tool-calling: 2-step task x3, correct tool + args?

Writes raw results to research/data/bench-<date>.jsonl and prints a summary table.
Usage: python3 scripts/bench_local_agents.py [model ...]
"""

import json
import os
import sys
import time
import urllib.request

MODELS = sys.argv[1:] or ["llama3.2:3b", "qwen3:14b", "muse-glimmer:30b-mlx"]
OLLAMA = "http://localhost:11434/api/chat"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = time.strftime("%Y-%m-%d")
OUT = os.path.join(ROOT, "research", "data", f"bench-{DATE}.jsonl")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

LOREM = ("The deployment pipeline reads configuration from three sources in order: "
         "environment variables, the project manifest, and the fallback defaults. ") * 60  # ~1k tokens

JSON_TASK = """Extract the following into JSON with EXACTLY these keys:
{"name": string, "stars": integer, "language": string, "archived": boolean}
Repository: nooa-agents, written in Python, 4821 stars, actively maintained.
Answer with the JSON object only. No markdown, no explanation."""

JSON_KEYS = {"name": str, "stars": int, "language": str, "archived": bool}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_stock",
        "description": "Get current stock count for an item",
        "parameters": {"type": "object",
                       "properties": {"item": {"type": "string"}},
                       "required": ["item"]},
    },
}]
TOOL_TASK = "How many oranges are in stock? Use the tool."


def chat(model, messages, tools=None, num_predict=600):
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"num_predict": num_predict, "temperature": 0}}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    d["_wall_s"] = round(time.time() - t0, 1)
    return d


def rate(count, dur_ns):
    return round(count / (dur_ns / 1e9), 1) if dur_ns else None


def log(rec):
    with open(OUT, "a") as f:
        f.write(json.dumps(rec) + "\n")


def approx_tokens(s):
    return len(s) // 4


results = {}
for model in MODELS:
    print(f"\n=== {model} ===", flush=True)
    r = {}

    chat(model, [{"role": "user", "content": "hi"}], num_predict=20)  # warm up

    d = chat(model, [{"role": "user", "content": LOREM + "\nSummarize in one sentence."}])
    r["prompt_tok_s"] = rate(d.get("prompt_eval_count", 0), d.get("prompt_eval_duration", 0))
    r["gen_tok_s"] = rate(d.get("eval_count", 0), d.get("eval_duration", 0))
    log({"model": model, "test": "speed", "prompt_tok_s": r["prompt_tok_s"],
         "gen_tok_s": r["gen_tok_s"], "prompt_tokens": d.get("prompt_eval_count"),
         "wall_s": d["_wall_s"]})
    print(f"  speed: prompt {r['prompt_tok_s']} tok/s, gen {r['gen_tok_s']} tok/s "
          f"(wall {d['_wall_s']}s)", flush=True)

    valid = conform = 0
    think_tokens, walls = [], []
    for i in range(5):
        d = chat(model, [{"role": "user", "content": JSON_TASK}])
        msg = d.get("message", {})
        content = (msg.get("content") or "").strip()
        think_tokens.append(approx_tokens(msg.get("thinking") or ""))
        walls.append(d["_wall_s"])
        ok_valid = ok_conform = False
        try:
            if content.startswith("```"):
                content = content.strip("`").lstrip("json").strip()
            obj = json.loads(content)
            ok_valid = True
            ok_conform = (set(obj) == set(JSON_KEYS)
                          and all(isinstance(obj[k], t) for k, t in JSON_KEYS.items()))
        except Exception:
            pass
        valid += ok_valid
        conform += ok_conform
        log({"model": model, "test": "json", "run": i, "valid": ok_valid,
             "conform": ok_conform, "thinking_tokens_approx": think_tokens[-1],
             "wall_s": d["_wall_s"], "content_head": content[:120]})
    r["json"] = f"{conform}/5 (valid {valid}/5)"
    r["json_avg_wall"] = round(sum(walls) / len(walls), 1)
    r["json_avg_think"] = sum(think_tokens) // len(think_tokens)
    print(f"  json: conform {r['json']}, avg {r['json_avg_wall']}s/call, "
          f"~{r['json_avg_think']} thinking tokens/call", flush=True)

    tool_ok = 0
    for i in range(3):
        try:
            d = chat(model, [{"role": "user", "content": TOOL_TASK}], tools=TOOLS)
            calls = d.get("message", {}).get("tool_calls") or []
            ok = any(c.get("function", {}).get("name") == "get_stock"
                     and "orange" in json.dumps(
                         c.get("function", {}).get("arguments", {})).lower()
                     for c in calls)
        except Exception as e:
            ok, calls = False, str(e)[:80]
        tool_ok += ok
        log({"model": model, "test": "tools", "run": i, "ok": ok,
             "calls": calls if isinstance(calls, str) else len(calls)})
    r["tools"] = f"{tool_ok}/3"
    print(f"  tools: {r['tools']}", flush=True)
    results[model] = r

print("\n\n=== SUMMARY ===")
print(f"{'model':<24} {'prompt t/s':>10} {'gen t/s':>8} {'json':>16} "
      f"{'s/call':>7} {'think':>6} {'tools':>6}")
for m, r in results.items():
    print(f"{m:<24} {r['prompt_tok_s']:>10} {r['gen_tok_s']:>8} {r['json']:>16} "
          f"{r['json_avg_wall']:>7} {r['json_avg_think']:>6} {r['tools']:>6}")
print(f"\nraw: {OUT}")
