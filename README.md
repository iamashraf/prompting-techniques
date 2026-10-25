# Prompting Techniques

A hands-on, runnable comparison of core LLM prompting techniques —
built to understand each one by actually running it against the same
task and the same data, not just reading about it.

Each technique (Zero-Shot, One-Shot, Few-Shot, Chain-of-Thought,
Tree-of-Thought, Parameter Tuning — from a prompt-engineering course —
plus Self-Consistency, Prompt Chaining, Structured Output, and ReAct
beyond it) is its own small, standalone Python module. Every one was
run for real against a local model, and what actually happened —
including the mistakes, the fabrications, and the surprises — is
written up honestly, not just asserted. If you're learning prompt
engineering, this is meant to be read, run, and modified, not just
glanced at.

## Status

✅ All 10 techniques from the original scope are built, tested, and
documented. Each one was added as its own reviewed step and run for
real. Open to more techniques landing here the same way.

## Goals

- Every technique is a small, standalone module you can run on its own.
- The same example task is used across techniques, so outputs are
  genuinely comparable.
- Code favors clarity over cleverness — this is meant to be read by
  people learning the concepts, not just executed.

## Getting started

```bash
uv sync
```

### Prerequisites

A running [Ollama](https://ollama.com) instance reachable at
`http://localhost:11434`, with the model pulled. Easiest path:

```bash
./scripts/ensure_ollama.sh
```

This reuses an already-running Ollama if you have one and starts
nothing new; otherwise it starts one via `docker-compose.yml`. Or set
it up yourself with a plain `ollama pull llama3.1:8b` if you'd rather
not use Docker/Podman at all.

### Running a technique

Each technique is a standalone, runnable module:

```bash
uv run python -m prompting_techniques.techniques.zero_shot
```

This prints the exact prompt sent to the model, the generated report,
and the path of a full run log saved under `runs/<technique>/` (one
`.txt` file per run, gitignored: generated output, not source).

### Comparing techniques

```bash
uv run python -m prompting_techniques.judge
```

Scores each technique against the one before it in the escalation, on
a rubric (Groundedness, Completeness, Business Reasoning, Structure,
Actionability, Executive Readiness) — see
[docs/findings.md](docs/findings.md) for why it judges pairwise rather
than all at once.

### Running tests

```bash
uv run pytest
```

Tests are fast and network-free — they never call the model.

## Experimentation

Beyond building each technique once, several threads of
experimentation ran across the project, each testing a specific
question rather than just producing a nicer report:

- **Reproducibility** — same prompt, same temperature, run twice: is
  the output actually deterministic? (`zero_shot_experiments.py`,
  `one_shot_experiments.py`)
- **Example quality** — does a mismatched or incomplete worked example
  hurt more than the technique itself helps? (`one_shot_experiments.py`;
  the answer for Few-Shot was yes)
- **LLM-as-judge reliability** — does naming "Groundedness" as a rubric
  criterion make a judge actually catch a fabrication? Does switching
  judge models? No and no — what worked was forcing explicit
  claim-by-claim verification before scoring (`judge.py`)
- **Scale** — does a bigger, more complex dataset change which
  technique wins? Running at 25 events (`scripts/compare_at_scale.py`)
  surfaced something bigger than planned: every technique silently
  reasoned about only the last ~9 events and dropped the rest
- **Parameters** — temperature, max_tokens, and top_p swept one at a
  time against a fixed Chain-of-Thought prompt (`parameter_tuning.py`)

## Learn more

- [docs/findings.md](docs/findings.md) — what each technique's
  experiments actually showed.
- [docs/layout.md](docs/layout.md) — how the code is organized.
