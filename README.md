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

(Run instructions for individual techniques will be documented here as
each one is built.)

## Layout

```
src/prompting_techniques/   # library code
```

More structure (techniques/, scenarios/, an LLM client, etc.) will be
documented here as it's built, not before.
