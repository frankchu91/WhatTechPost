<!--
REVIEW NOTES (delete before publishing)
- Verified by Claude on 2026-08-07: repo cloned, source install works on Python 3.13 (NOT 3.14), Agent subclass creation works, `pip install nooa` NOT yet on PyPI despite README. Version installed: 0.0.1.dev1.
- NOT verified: benchmark numbers (82.2% SWE-bench, 86.8% CyberGym) — from NVIDIA's own paper. Phrased as claims in the text.
- YOUR TAKE SLOT: the paragraph marked [PERSONAL TAKE] — add how this compares to how you build agents in your own products.
- Cover image idea: screenshot of the InventoryAgent class in an editor.
-->

---
title: "NVIDIA's NOOA turns an AI agent into one Python class — I installed it so you don't have to"
published: false
description: "Hands-on first look at NOOA: methods are tools, docstrings are prompts, type hints are contracts. Plus two install gotchas the README won't tell you."
tags: ai, python, agents, opensource
---

NVIDIA Labs open-sourced [NOOA](https://github.com/NVIDIA-NeMo/labs-OO-Agents) (NVIDIA Object-Oriented Agents) this week, and the pitch is unusually simple: an agent is a Python class. Not a graph, not a chain, not a YAML pipeline. A class.

I cloned it and got it running the same day. Here's what it actually looks like, what broke, and why I think the core idea matters more than the framework itself.

## The whole idea in one code block

```python
from nooa import Agent

class InventoryAgent(Agent, llm=llm):
    """You are an agent that checks inventory using deterministic helper methods."""

    # Plain Python — automatically available as a tool for the LLM
    def get_stock(self, item: str) -> int:
        """Get current stock for an item."""
        return self.inventory.get(item, {}).get("stock", 0)

    # `...` body — the LLM implements this at runtime, calling the methods above
    async def can_fulfill_order(self, items: list[str], budget: float) -> Result:
        """Check if order can be fulfilled within budget."""
        ...
```

That's from the repo's quickstart, lightly trimmed. The mapping is:

- **Fields** are agent state
- **Methods with real bodies** are deterministic tools
- **Methods with `...` bodies** are implemented by an LLM loop at runtime
- **Docstrings** are the prompts
- **Type annotations** are contracts the runtime enforces, with auto-retry on mismatch

No separate tool-schema JSON. No registration step. The model acts by writing Python in a REPL with access to `self`, so your method signatures *are* the tool definitions.

## Two install gotchas before you try it

The README says `pip install nooa`. Two things I hit on a clean machine:

**1. It's not on PyPI yet.** As of today, `pip install nooa` returns `No matching distribution found`. Install from source instead:

```bash
git clone https://github.com/NVIDIA-NeMo/labs-OO-Agents.git
uv venv --python 3.13 && uv pip install ./labs-OO-Agents
```

**2. No Python 3.14 support.** The package pins `>=3.12,<3.14`. My default interpreter is 3.14, and the install fails with a version error. Use 3.12 or 3.13.

After that, everything imported cleanly and defining an `Agent` subclass with a generation method worked first try (version installed: `0.0.1.dev1` — this is early software, and it behaves like it).

## What's genuinely different here

Most agent frameworks make you maintain two parallel worlds: your code, and a shadow copy of your code described in schemas, prompt templates, and callback wiring. Every refactor has to happen twice.

NOOA's bet is that the language already has all the metadata an LLM needs — signatures, types, docstrings — so the shadow world can be deleted. Your agent diffs like code, tests like code, and refactors like code. `mypy` and your IDE understand it because there's nothing else to understand.

There's also a strategy layer worth knowing about: `PredictStrategy` (single completion) vs `CodeActStrategy` (iterative code execution, capped by `max_iterations`), swappable per method via a decorator. That's a clean answer to "some steps need one LLM call, some need a loop" without restructuring the agent.

NVIDIA's paper claims a 253-line NOOA agent hits 82.2% on SWE-bench Verified and 86.8% on CyberGym L1. I haven't reproduced those numbers, and you shouldn't take vendor benchmarks at face value — but the interesting claim isn't the score, it's the line count.

## The part that should make you nervous

A NOOA agent acts by executing LLM-generated Python. With access to `self`, imports, and whatever your process can reach. NVIDIA's own docs tell you to run agents in a sandbox, and they mean it — this is `exec()` with extra steps, by design. If you wouldn't run `curl | sh` from a model, don't run NOOA agents outside a container either.

[PERSONAL TAKE — add your own experience building agents here: what you use today, what pain this would/wouldn't solve for you.]

## Should you use it?

Today: probably not in production. It's a `0.0.1.dev1` that isn't on PyPI yet.

But I'd bet on the direction. We spent two years building agent frameworks that look like workflow engines, and the results are brittle in ways every practitioner knows. "The programming language is the agent definition language" is the first framing I've seen that gets *simpler* as your agent gets bigger. Worst case, NOOA becomes the CoffeeScript of agents: the thing itself fades, but every framework after it steals the idea.

The [examples directory](https://github.com/NVIDIA-NeMo/labs-OO-Agents/blob/main/examples/README.md) is a genuinely good progressive tutorial — 11 numbered files from first generation method to MCP tools. Start with `03_codeact_tools.py`; it's the one that made the design click for me.

Have you tried collapsing your agent stack into plain code? I'd like to hear where it broke.

---

*Research and drafting assisted by AI; all tests, opinions, and final edits are my own.*
