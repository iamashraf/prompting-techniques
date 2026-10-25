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
`http://localhost:11434` (locally installed, or a container — either
works), with the model pulled:

```bash
ollama pull llama3.1:8b
```

### Running a technique

Each technique is a standalone, runnable module:

```bash
uv run python -m prompting_techniques.techniques.zero_shot
```

This prints the exact prompt sent to the model, the generated report,
and the path of a full run log saved under `runs/` — one `.txt` file per
run, containing the exact system prompt, user prompt, and response
(gitignored: generated output, not source).

### Running the experiments

Most techniques have a companion `..._experiments.py` module that
isolates one nuance or failure mode per function (e.g. does output
change run-to-run? does the model invent numbers when data is missing?):

```bash
uv run python -m prompting_techniques.techniques.zero_shot_experiments
```

These make real calls to your local model and can take a few minutes.

### Running tests

```bash
uv run pytest
```

Tests are fast and network-free — they never call the model.

## Findings

- [Zero-Shot](docs/zero-shot-findings.md) — what the experiments actually
  showed, in plain terms.

## Layout

```
data/                              # shared example scenario (CSV)
runs/                              # generated prompt+response logs (gitignored)
src/prompting_techniques/
  scenario.py                      # loads the data, builds the shared business_context text
  run_log.py                       # persists every prompt+response under runs/
  techniques/
    zero_shot.py                   # the technique itself
    zero_shot_experiments.py       # hands-on experiments exploring its nuances
tests/
```

More techniques land here the same way, one reviewed step at a time.
