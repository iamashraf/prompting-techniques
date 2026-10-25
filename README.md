# Prompting Techniques

Runnable, side-by-side Python implementations of core LLM prompting
techniques — built to understand each one by running and comparing it,
not just reading about it.

This repo grew out of a prompt-engineering course session (Zero-Shot,
One-Shot, Few-Shot, Chain-of-Thought, Tree-of-Thought, parameter tuning,
and LLM-as-judge evaluation), extended with a few techniques beyond the
course (self-consistency, prompt chaining, structured output, ReAct).

## Status

🚧 Under active, incremental construction. Each technique is added as its
own reviewed step — nothing here is generated in bulk. Expect this
section and the layout below to grow one module at a time.

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

This reuses an already-running Ollama if you have one (e.g. from a
sibling project) and starts nothing new; otherwise it starts one via
`docker-compose.yml`, sharing the same model volume as the
`research-assistant` project so nothing gets re-downloaded. Override
which judge model gets pulled with `JUDGE_MODEL`:

```bash
JUDGE_MODEL=phi3:mini ./scripts/ensure_ollama.sh
```

Or set it up yourself with a plain `ollama pull llama3.1:8b` if you'd
rather not use Docker/Podman at all.

### Running a technique

Each technique is a standalone, runnable module:

```bash
uv run python -m prompting_techniques.techniques.zero_shot
```

This prints the exact prompt sent to the model, the generated report,
and the path of a full run log saved under `runs/<technique>/` — one
`.txt` file per run, containing the exact system prompt, user prompt,
and response (gitignored: generated output, not source).

### Running the experiments

Most techniques have a companion `..._experiments.py` module that
isolates one nuance or failure mode per function (e.g. does output
change run-to-run? does the model invent numbers when data is missing?):

```bash
uv run python -m prompting_techniques.techniques.zero_shot_experiments
```

These make real calls to your local model and can take a few minutes.

### Comparing techniques

Once two or more techniques exist, `judge.py` scores their baseline
reports side by side (same 1-5 rubric the course used: Completeness,
Business Reasoning, Structure, Actionability, Executive Readiness):

```bash
uv run python -m prompting_techniques.judge
```

### Running tests

```bash
uv run pytest
```

Tests are fast and network-free — they never call the model.

## Findings

- [Zero-Shot](docs/zero-shot-findings.md) — what the experiments actually
  showed, in plain terms.
- [One-Shot](docs/one-shot-findings.md) — including a scored comparison
  against Zero-Shot, and what the score missed.
- [Few-Shot](docs/few-shot-findings.md) — a lesson about example quality
  that mattered more than the technique itself.
- [Chain-of-Thought](docs/chain-of-thought-findings.md) — the first
  technique that actually fixed the arithmetic problem.

## Layout

```
docker-compose.yml                 # optional local Ollama, sharing research-assistant's model volume
scripts/ensure_ollama.sh           # starts Ollama only if nothing's already running
data/                              # shared example scenario (CSV)
runs/                              # generated prompt+response logs (gitignored)
src/prompting_techniques/
  scenario.py                      # loads the data, builds the shared business_context text
  run_log.py                       # persists every prompt+response under runs/
  ollama_client.py                 # the one shared call to a local Ollama model
  judge.py                         # LLM-as-judge: scores techniques' reports side by side
  techniques/
    zero_shot.py                   # the technique itself
    zero_shot_experiments.py       # hands-on experiments exploring its nuances
    one_shot.py                    # zero-shot + exactly one worked example
    one_shot_experiments.py        # experiments specific to adding an example
    few_shot.py                    # zero-shot + several worked examples
    chain_of_thought.py            # reason step by step, then write the report
tests/
```

More techniques land here the same way, one reviewed step at a time.
