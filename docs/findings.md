# Findings

What each technique's experiments actually showed, written up honestly
— including the mistakes and the surprises, not just the wins.

- [Zero-Shot](zero-shot-findings.md) — what the experiments actually
  showed, in plain terms.
- [One-Shot](one-shot-findings.md) — including a scored comparison
  against Zero-Shot, and what the score missed.
- [Few-Shot](few-shot-findings.md) — a lesson about example quality
  that mattered more than the technique itself.
- [Chain-of-Thought](chain-of-thought-findings.md) — the first
  technique that actually fixed the arithmetic problem.
- [Tree-of-Thought](tree-of-thought-findings.md) — better-justified
  mitigation choices, but that discipline didn't carry over to arithmetic.
- [Self-Consistency](self-consistency-findings.md) — a safety net
  that only shows its value once something is unstable enough to need it.
- [Prompt Chaining](prompt-chaining-findings.md) — correctness by
  freezing results forward, not by reasoning better in any one step.
- [Structured Output](structured-output-findings.md) — perfect
  JSON shape, wrong totals, caught with three lines of Python.
- [ReAct](react-findings.md) — the only technique where the total
  is correct by construction, not by luck — at the cost of writing and
  securing real code instead of just a better prompt.
- [Parameter Tuning](parameter-tuning-findings.md) — high
  temperature doesn't just add noise, it fabricates facts with full
  confidence; max_tokens is a hard requirement, not a cosmetic knob.
